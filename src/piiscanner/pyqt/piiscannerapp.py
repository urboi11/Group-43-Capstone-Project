from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QLabel, QPushButton
from PySide6.QtCore import QSize
from PySide6 import QtCore, QtGui, QtWidgets
import json, fnmatch, pathlib, time, yaml, os, webbrowser
from ..modelbackend.infer import PiiModel
from ..modelbackend.utils import read_any, merge_findings
import logging
import datetime as dt
import regex as re
from pathlib import Path
from .piiscannerform import Ui_Form
from .piiscannersettings import SettingsPanel
from .piiscannerwarning import PopUpForWarning



## TODO: Set up logging location.
class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

        self.settingsPanel = SettingsPanel()

        self.popUpWindow = None

        self.fileLocation = None

        self.setupUi(self)

        self.setFixedSize(QSize(650,500))

        self.ProgressBar.setMinimum(0)
        
        self.ProgressBar.setMaximum(100)

        self.FileBrowseButton.clicked.connect(self.open_file_browser)

        self.DirectoriesBrowseButton.clicked.connect(self.open_directory_browser)


        self.ScanFilesButton.clicked.connect(lambda: self.switch_to_file_panel(2))

        self.ScanDirectoryButton.clicked.connect(lambda: self.switch_to_file_panel(1))
        
        self.FileMainMenuButton.clicked.connect(lambda: self.switch_to_main_menu_panel(0))

        self.DirectoriesMainMenuButton.clicked.connect(lambda: self.switch_to_main_menu_panel(0))

        # self.FileScanNowButton.clicked.connect(self.scan)

        # self.DirectoryScanNowButton.clicked.connect(self.scan)

        self.ResultsMainMenuButton.clicked.connect(self.switch_to_main_menu_panel)
        
        self.FindingsFolderButton.clicked.connect(lambda: self.open_external_document(self.fileLocation))

        self.FileSettingsMenu.clicked.connect(self.open_settings)
        
    def open_settings(self):
  
            if self.settingsPanel.ssnValue != 0.0:
                self.settingsPanel.double_spin_box_ssn.setValue(float(self.settingsPanel.ssnValue))

            if self.settingsPanel.emailValue != 0.0:
                self.settingsPanel.double_spin_box_email.setValue(float(self.settingsPanel.emailValue))
            
            if self.settingsPanel.phoneValue != 0.0:
                self.settingsPanel.double_spin_box_phone.setValue(float(self.settingsPanel.phoneValue))

            if self.settingsPanel.personValue != 0.0:
                self.settingsPanel.double_spin_box_phone.setValue(float(self.settingsPanel.personValue))

            if self.settingsPanel.cardValue != 0.0:
                self.settingsPanel.double_spin_box_card.setValue(float(self.settingsPanel.cardValue))
 
            if self.settingsPanel.dobValue != 0.0:
                self.settingsPanel.double_spin_box_dob.setValue(float(self.settingsPanel.dobValue))

            if self.settingsPanel.IPAddressValue != 0.0:
                self.settingsPanel.double_spin_box_ip_address.setValue(float(self.settingsPanel.IPAddressValue))

            if self.settingsPanel.addressValue != 0.0:
                self.settingsPanel.double_spin_box_address.setValue(float(self.settingsPanel.addressValue))

            if self.settingsPanel.outputLocation != "":
                self.settingsPanel.outputLineEdit.setText(self.settingsPanel.outputLocation)

            if self.settingsPanel.loggingLocation != "":
                self.settingsPanel.loggingLineEdit.setText(self.settingsPanel.loggingLocation)
            
            if self.settingsPanel.batchSizeValue != 0:
                self.settingsPanel.spin_box_batch_size.setValue(int(self.settingsPanel.batchSizeValue))
            
            if self.settingsPanel.mergeGapValue != 0:
                self.settingsPanel.spin_box_merge_gap.setValue(int(self.settingsPanel.mergeGapValue))

            self.settingsPanel.show()

        
    
    def open_file_browser(self):
        fileName = QFileDialog.getOpenFileName(self, "Find Files..", os.getcwd(), "Text Files (*.txt);;Word Files (*.docx);;PDF Files(*.pdf)")
        self.FileLineEdit.setText(fileName[0])
        
    def open_directory_browser(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.DirectoryLineEdit.setText(directory)

    def switch_to_file_panel(self, index):
        self.stackedWidget.setCurrentIndex(index)
    
    def switch_to_file_panel_scan(self, index, scan):
        self.ProgressBar.setValue(0)
        self.stackedWidget.setCurrentIndex(index)
        scan()
    
    def switch_to_main_menu_panel(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.FileLineEdit.setText("")
        self.DirectoryLineEdit.setText("")
        self.FileResults.setText("")
    
    def open_external_document(self, fileName):
        os.open(fileName)

    def scan(self):
        try:
            pattern = "^(.+[/\\\\])?([^/\\\\]+)$"
            if re.match(pattern, self.FileLineEdit.text()) or re.match(pattern, self.DirectoryLineEdit.text()):
                
                
                self.stackedWidget.setCurrentIndex(3)

                thresholds = {
                    "SSN" : float(self.settingsPanel.ssnValue),
                    "EMAIL" : float(self.settingsPanel.emailValue),
                    "PHONE" : float(self.settingsPanel.phoneValue),
                    "PERSON" : float(self.settingsPanel.personValue),
                    "CREDIT_CARD": float(self.settingsPanel.cardValue),
                    "DOB" : float(self.settingsPanel.dobValue),
                    # "ADDRESS" : float(self.settingsPanel.add)
                    # "IP_ADDRESS" : 
                }
                model = PiiModel(
                    model_dir=self.cfg.get("model_dir", "model"),
                    thresholds=self.cfg.get("thresholds", {}),
                    batch_size=self.settingsPanel.batchSizeValue,
                )
        
                self.ProgressBar.setValue(25)

                #Build File List 
                paths = []
                if len(self.FileLineEdit.text()) > 0:
                    os.path.isfile(self.FileLineEdit.text())
                    if os.path.isfile(self.FileLineEdit.text()):
                        paths.append(self.FileLineEdit.text())
                elif len(self.DirectoryLineEdit.text()) > 0:
                    if os.path.isdir(self.DirectoryLineEdit.text()):
                        for root, _, files in os.walk(self.DirectoryLineEdit.text()):
                            if any(fnmatch.fnmatch(root, ex) for ex in self.cfg.get("exclude_globs", [])):
                                continue
                            for f in files:
                                paths.append(os.path.join(root, f))
        
                self.ProgressBar.setValue(50)

                merged = []
                if paths:
                    for p in paths:
                        text = read_any(p)
                        if not text:
                            continue
                        findings = model.predict(text)
                        file_merged = merge_findings(findings, max_gap=self.cfg.get("merge_gap", 0))
                        fname = pathlib.Path(p).name
                        for f in file_merged:
                            merged.append({**f, "file": fname})

                self.ProgressBar.setValue(75)

                if merged:
                    record = {
                        "ts": time.time(),
                        "files": [pathlib.Path(p).name for p in paths],
                        "findings": merged,
                    }

                    with open(str(self.outputDir + os.path.sep + (pathlib.Path(p).name + ".json")), "w") as file:
                        file.write(json.dumps(record, indent=2))
                        self.FileResults.setText(json.dumps(record, indent=2))

                        self.fileLocation = self.outputDir + os.path.sep + (pathlib.Path(p).name + ".json")
                            
                        file.close()
                        self.ProgressBar.setValue(100)
                        self.stackedWidget.setCurrentIndex(4)          
                else:
                    self.stackedWidget.setCurrentIndex(0)
                    self.popUpWindow = PopUpForWarning()
                    self.popUpWindow.setText("This file or directory does not have any PII data!")
                    self.popUpWindow.show()


    
            else:
                if len(self.FileLineEdit.text()) == 0 or len(self.FileLineEdit.text()) == 0:
                    self.popUpWindow = PopUpForWarning()
                    self.popUpWindow.setText("Please make sure you have a File or Directory selected before scanning!")
                    self.popUpWindow.show()

        except Exception as E:
            logging.basicConfig(filename=self.cfg["logging"]["file"] + os.path.sep + str(dt.datetime.now().strftime('%y-%m-%d-Time-%H-%M')) + ".log" , filemode="a", format="%(asctime)s - %(levelname)s - %(message)s" )
            self.logger = logging.getLogger(__name__)
        
            self.logger.error("%s", E, exc_info=True)
            
