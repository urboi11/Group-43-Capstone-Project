from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QLabel, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
import json, fnmatch, pathlib, time, yaml, os, webbrowser
from ..modelbackend.infer import PiiModel
from ..modelbackend.utils import read_any, merge_findings
import logging, sys, platform, stat
import datetime as dt
import regex as re
from pathlib import Path
from .piiscannerform import Ui_Form
from .piiscannersettings import SettingsPanel
from .piiscannerwarning import PopUpForWarning
from ctypes import wintypes, byref
import ctypes
import subprocess
from collections import defaultdict



# Define Constants
SEE_MASK_NOCLOSEPROCESS = 0x00000040
INFINITE = 0xFFFFFFFF

# Define the Structure for ShellExecuteEx
class SHELLEXECUTEINFOW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("fMask", wintypes.ULONG),
        ("hwnd", wintypes.HWND),
        ("lpVerb", wintypes.LPCWSTR),
        ("lpFile", wintypes.LPCWSTR),
        ("lpParameters", wintypes.LPCWSTR),
        ("lpDirectory", wintypes.LPCWSTR),
        ("nShow", ctypes.c_int),
        ("hInstApp", wintypes.HINSTANCE),
        ("lpIDList", wintypes.LPVOID),
        ("lpClass", wintypes.LPCWSTR),
        ("hkeyClass", wintypes.HKEY),
        ("dwHotKey", wintypes.DWORD),
        ("hMonitor", wintypes.HANDLE),
        ("hProcess", wintypes.HANDLE),
    ]



class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

        self.settingsPanel = SettingsPanel()

        self.popUpWindow = None

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

        self.FileScanNowButton.clicked.connect(self.scan)

        self.DirectoryScanNowButton.clicked.connect(self.scan)

        self.ResultsMainMenuButton.clicked.connect(self.switch_to_main_menu_panel)
        
        self.FindingsFolderButton.clicked.connect(lambda: os.open(self.outputDir, os.O_RDWR))

        self.FileSettingsMenu.clicked.connect(self.open_settings)

        self.DirectorySettingsMenu.clicked.connect(self.open_settings)
        
        
        if platform.system() == "Darwin":
            resourceFolder = "/Applications/pii-scanner.app/Contents/Resources"
            
            self.settingsPanel.outputLocation = "/Applications/pii-scanner.app/Contents/Resources/Output"
            self.settingsPanel.loggingLocation = "/Applications/pii-scanner.app/Contents/Resources/Logging"
            
            if Path(self.settingsPanel.outputLocation).is_dir() == False or Path(self.settingsPanel.loggingLocation).is_dir() == False:

                os.system(f"osascript -e 'do shell script \"chmod o+w {resourceFolder}\" with administrator privileges'")
        
                os.makedirs(self.settingsPanel.outputLocation)
                os.makedirs(self.settingsPanel.loggingLocation)

        if platform.system() == "Windows":
            
            os.chdir("C:\\Program Files\\pii-scanner\\app\\piiscanner\\pyqt\\resources")

            window_icon = QIcon()
            
            window_icon.addFile("icon.png")

            self.setWindowIcon(window_icon)

            self.settingsPanel.outputLocation = "C:\\Program Files\\pii-scanner\\findings\\"
            self.settingsPanel.loggingLocation = "C:\\Program Files\\pii-scanner\\logs\\"

            self.is_admin()                
            command = f'/c icacls "C:\\Program Files\\pii-scanner" /grant:r "Users":(OI)(CI)M /T'
            if self.is_admin() == 1:

                result = subprocess.run(command, shell=True, check=True, 
                                capture_output=True, text=True)

                if Path(self.settingsPanel.outputLocation).is_dir() == False:
                    os.makedirs(self.settingsPanel.outputLocation)
                if Path(self.settingsPanel.loggingLocation).is_dir() == False:
                    os.makedirs(self.settingsPanel.loggingLocation)

            else:
                if Path(self.settingsPanel.outputLocation).is_dir() == False or Path(self.settingsPanel.loggingLocation).is_dir() == False:


                    sei = SHELLEXECUTEINFOW()
                    sei.cbSize = ctypes.sizeof(sei)
                    sei.fMask = SEE_MASK_NOCLOSEPROCESS # This is key to getting the process handle
                    sei.lpVerb = "runas"                # Admin elevation
                    sei.lpFile = "cmd.exe"
                    sei.lpParameters = command
                    sei.nShow = 0                    # SW_SHOWNORMAL


                    if ctypes.windll.shell32.ShellExecuteExW(byref(sei)):

                        ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, INFINITE)
                    
                        exit_code = wintypes.DWORD()
                        ctypes.windll.kernel32.GetExitCodeProcess(sei.hProcess, byref(exit_code))
                        
                        print(f"Command finished with exit code: {exit_code.value}")
                        
                        ctypes.windll.kernel32.CloseHandle(sei.hProcess)

                        if exit_code.value == 0:
                            os.makedirs(self.settingsPanel.outputLocation)

                            os.makedirs(self.settingsPanel.loggingLocation)

                    else:
                        print("Failed to launch process.")

                    

    def is_admin(self):
        try:
            IsUserAnAdmin = WinDLL("Shell32").IsUserAnAdmin
            return IsUserAnAdmin()
        except:
            return False
        
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

    def scan(self):
        try:
            if platform.system() == "Darwin":
                if self.settingsPanel.outputLocation != "/Applications/pii-scanner.app/Contents/Resources/Output":
                    self.settingsPanel.outputLocation = self.settingsPanel.outputLineEdit.text()
                if self.settingsPanel.loggingLocation != "/Applications/pii-scanner.app/Contents/Resources/Logging":
                    self.settingsPanel.loggingLocation = self.settingsPanel.loggingLineEdit.text()
                    
            
            if platform.system() == "Windows":

                if self.settingsPanel.outputLocation != "C:\\Program Files\\pii-scanner\\findings\\":
                    self.settingsPanel.outputLocation = self.settingsPanel.outputLineEdit.text()
                if self.settingsPanel.loggingLocation != "C:\\Program Files\\pii-scanner\\logs\\":
                    self.settingsPanel.loggingLocation = self.settingsPanel.loggingLineEdit.text()
            
            
            exclude_globs_list = ["\\node_modules\\", "\\.git\\"]
            thresholdsDict = {
                    "SSN" : float(self.settingsPanel.ssnValue),
                    "EMAIL" : float(self.settingsPanel.emailValue),
                    "PHONE" : float(self.settingsPanel.phoneValue),
                    "PERSON" : float(self.settingsPanel.personValue),
                    "CREDIT_CARD": float(self.settingsPanel.cardValue),
                    "DOB" : float(self.settingsPanel.dobValue),
                    "ADDRESS" : float(self.settingsPanel.addressValue),
                    "IP_ADDRESS" : float(self.settingsPanel.IPAddressValue)
                }
            
            pattern = "^(.+[/\\\\])?([^/\\\\]+)$"
            if re.match(pattern, self.FileLineEdit.text()) or re.match(pattern, self.DirectoryLineEdit.text()):
                
                
                self.stackedWidget.setCurrentIndex(3)

                model = PiiModel(
                    model_dir= "model",
                    thresholds=thresholdsDict,
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
                            if any(fnmatch.fnmatch(root, ex) for ex in exclude_globs_list):
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
                        file_merged = merge_findings(findings, max_gap=int(self.settingsPanel.mergeGapValue))
                        fname = pathlib.Path(p).name
                        for f in file_merged:
                            merged.append({**f, "file": fname})

                self.ProgressBar.setValue(75)

                if merged:
                    ## TODO: Reorder structure. 
                    record = {
                        "ts": time.time(),
                        "files": [pathlib.Path(p).name for p in paths],
                        "findings": merged,
                    }
                    #TODO: the file name should also be based on if it is either a directory or a file.
                    self.outputDir = self.settingsPanel.outputLocation + os.path.sep + (pathlib.Path(p)).name + "-" + str(dt.datetime.now().strftime('%y-%m-%d-Time-%H-%M-%S')) + ".jsonl" 
                    with open(self.outputDir, "w") as file:
                        file.write(json.dumps(record))
                        file.write("\r\n")
                        #parsing JSON for display
                        results = []
                        currentFile = None
                        for f in record.get("findings",[]):
                                if f['file'] != currentFile:
                                    currentFile = f['file']
                                    
                                    # Count label types for this file
                                    label_counts = defaultdict(int)
                                    for finding in record.get("findings", []):
                                        if finding['file'] == currentFile:
                                            label_counts[finding['label']] += 1
                                    
                                    # Display file header and counts
                                    results.append("")
                                    results.append(f"====={currentFile}=====")
                                    for label, count in sorted(label_counts.items()):
                                        results.append(f"  {label}: {count}")
                        self.FileResults.setText("\n".join(results))
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
            logging.basicConfig(filename=self.settingsPanel.loggingLocation + os.path.sep + str(dt.datetime.now().strftime('%y-%m-%d-Time-%H-%M')) + ".log" , filemode="a", format="%(asctime)s - %(levelname)s - %(message)s" )

            self.logger = logging.getLogger(__name__)
        
            self.logger.error("%s", E, exc_info=True)
            