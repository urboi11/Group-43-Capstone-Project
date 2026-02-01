# infer.py (ONNX, robust local loading + long-text chunking)
from __future__ import annotations
 
from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import json, os, sys
from pathlib import Path
 
 
def _resource_path(rel_path: str | os.PathLike) -> Path:
    # Works in both source and PyInstaller EXE
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return (base / rel_path).resolve()
 
 
def _base_label(lbl: str) -> str:
    return lbl[2:] if lbl and (lbl.startswith("B-") or lbl.startswith("I-")) else lbl
 
 
class PiiModel:
    """
    ONNX-backed token classifier that supports long documents by chunking
    into <=512-token windows (DistilBERT positional limit).
    """
    def __init__(self, model_dir="model", thresholds=None, batch_size=8, max_len=512, stride=64):
        mdir = Path(model_dir)
        self.model_dir = mdir if mdir.is_absolute() else _resource_path(mdir)
 
        # Force local files only (no internet)
        self.tok = AutoTokenizer.from_pretrained(str(self.model_dir), use_fast=True, local_files_only=True)
 
        model_path = self.model_dir / "model.onnx"
        if not model_path.exists():
            raise FileNotFoundError(f"model.onnx not found at: {model_path}")
 
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
 
        id2label_path = self.model_dir / "id2label.json"
        if not id2label_path.exists():
            raise FileNotFoundError(f"id2label.json not found at: {id2label_path}")
 
        with open(id2label_path, "r", encoding="utf-8") as f:
            self.id2label = {int(k): v for k, v in json.load(f).items()}
 
        self.thresholds = thresholds or {}
        self.default_threshold = float(self.thresholds.get("DEFAULT", 0.5))
 
        # For DistilBERT/token-classification exports, 512 is the safe max.
        self.max_len = int(max_len)
        self.stride = int(stride)
        self.batch_size = batch_size  # not used in this simple implementation
 
    def _threshold_for(self, label_full: str) -> float:
        """
        Apply thresholds using base label first:
          thresholds["ADDRESS"] -> applies to "B-ADDRESS"/"I-ADDRESS"
        Fallbacks:
          thresholds[label_full] then thresholds["DEFAULT"] then 0.5
        """
        base = _base_label(label_full)
        if base in self.thresholds:
            return float(self.thresholds[base])
        if label_full in self.thresholds:
            return float(self.thresholds[label_full])
        return float(self.default_threshold)
 
    def _run_chunk(self, input_ids_chunk, attention_chunk):
        inputs = {
            "input_ids": np.array([input_ids_chunk], dtype=np.int64),
            "attention_mask": np.array([attention_chunk], dtype=np.int64),
        }
        (logits,) = self.session.run(None, inputs)  # [1, T, C]
        logits = logits[0]
        # stable softmax
        logits = logits - logits.max(axis=-1, keepdims=True)
        exps = np.exp(logits)
        probs = exps / exps.sum(axis=-1, keepdims=True)
        return probs  # [T, C]
 
    def predict(self, text: str):
        """
        Returns token-level findings (fragments) with character offsets into the ORIGINAL text.
        Safe for long documents via token chunking.
        """
        if not text:
            return []
 
        # Tokenize WITHOUT truncation so we can chunk ourselves.
        enc = self.tok(text, return_offsets_mapping=True, truncation=False)
 
        input_ids = enc["input_ids"]
        attention = enc["attention_mask"]
        offsets = enc["offset_mapping"]  # list of (char_start, char_end)
 
        n = len(input_ids)
        if n == 0:
            return []
 
        findings = []
        seen = set()  # de-dupe exact (start,end,label)
 
        start_idx = 0
        while start_idx < n:
            end_idx = min(start_idx + self.max_len, n)
 
            ids_chunk = input_ids[start_idx:end_idx]
            attn_chunk = attention[start_idx:end_idx]
            off_chunk = offsets[start_idx:end_idx]
 
            probs = self._run_chunk(ids_chunk, attn_chunk)
 
            for i, (cstart, cend) in enumerate(off_chunk):
                if cend <= cstart:
                    continue
                lab_id = int(np.argmax(probs[i]))
                score = float(probs[i, lab_id])
                lab_full = self.id2label.get(lab_id, "O")
                if lab_full == "O":
                    continue
 
                thr = self._threshold_for(lab_full)
                if score >= thr:
                    key = (int(cstart), int(cend), lab_full)
                    if key not in seen:
                        seen.add(key)
                        findings.append({
                            "start": int(cstart),
                            "end": int(cend),
                            "label": lab_full,  # keep BIO tag if that’s what your model uses
                            "score": round(score, 4),
                        })
 
            if end_idx == n:
                break
            # overlap windows so entities split across boundaries can still be detected
            start_idx = max(0, end_idx - self.stride)
 
        return findings