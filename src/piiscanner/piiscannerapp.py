from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QLabel, QPushButton
from PySide6.QtCore import QSize, QObject
from PySide6 import QtCore, QtGui, QtWidgets
from .piiscanner import Ui_Form
import json, os, fnmatch, pathlib, time, yaml, os, webbrowser
from .infer import PiiModel
from .utils import read_any, merge_findings
import logging
import datetime as dt
import re
from os import startfile
from pathlib import Path


class Ui_SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400,400)

    def setupUi(self, SettingsPanel):
        SettingsPanel.setObjectName("SettingsPanel")
        SettingsPanel.resize(662, 420)
        self.thresholds_frame = QtWidgets.QFrame(SettingsPanel)
        self.thresholds_frame.setGeometry(QtCore.QRect(20, 20, 271, 301))
        self.thresholds_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.thresholds_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.thresholds_frame.setObjectName("thresholds_frame")
        self.lineEdit = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit.setGeometry(QtCore.QRect(180, 50, 71, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.thresholds_frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 101, 41))
        self.label.setMinimumSize(QtCore.QSize(101, 41))
        self.label.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 101, 41))
        self.label_2.setMinimumSize(QtCore.QSize(101, 41))
        self.label_2.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 101, 41))
        self.label_3.setMinimumSize(QtCore.QSize(101, 41))
        self.label_3.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 90, 71, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 120, 71, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_4.setGeometry(QtCore.QRect(20, 110, 101, 41))
        self.label_4.setMinimumSize(QtCore.QSize(101, 41))
        self.label_4.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 101, 41))
        self.label_5.setMinimumSize(QtCore.QSize(101, 41))
        self.label_5.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_6.setGeometry(QtCore.QRect(20, 180, 101, 41))
        self.label_6.setMinimumSize(QtCore.QSize(101, 41))
        self.label_6.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.thresholds_frame)
        self.label_7.setGeometry(QtCore.QRect(20, 210, 101, 41))
        self.label_7.setMinimumSize(QtCore.QSize(101, 41))
        self.label_7.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_7.setObjectName("label_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 160, 71, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(180, 190, 71, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.thresholds_frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(180, 220, 71, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.thresholds_frame_2 = QtWidgets.QFrame(SettingsPanel)
        self.thresholds_frame_2.setGeometry(QtCore.QRect(330, 20, 311, 141))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholds_frame_2.sizePolicy().hasHeightForWidth())
        self.thresholds_frame_2.setSizePolicy(sizePolicy)
        self.thresholds_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.thresholds_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.thresholds_frame_2.setObjectName("thresholds_frame_2")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.thresholds_frame_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(130, 50, 121, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_9 = QtWidgets.QLabel(self.thresholds_frame_2)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 101, 41))
        self.label_9.setMinimumSize(QtCore.QSize(101, 41))
        self.label_9.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setTextFormat(QtCore.Qt.AutoText)
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.thresholds_frame_2)
        self.label_10.setGeometry(QtCore.QRect(20, 80, 101, 41))
        self.label_10.setMinimumSize(QtCore.QSize(101, 41))
        self.label_10.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setTextFormat(QtCore.Qt.AutoText)
        self.label_10.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.thresholds_frame_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(130, 90, 121, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_15 = QtWidgets.QLabel(self.thresholds_frame_2)
        self.label_15.setGeometry(QtCore.QRect(0, 0, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.frame = QtWidgets.QFrame(SettingsPanel)
        self.frame.setGeometry(QtCore.QRect(330, 180, 311, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(0, 0, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(10, 30, 101, 41))
        self.label_11.setMinimumSize(QtCore.QSize(101, 41))
        self.label_11.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setTextFormat(QtCore.Qt.AutoText)
        self.label_11.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(10, 70, 101, 41))
        self.label_12.setMinimumSize(QtCore.QSize(101, 41))
        self.label_12.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setTextFormat(QtCore.Qt.AutoText)
        self.label_12.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_12.setObjectName("label_12")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_9.setGeometry(QtCore.QRect(180, 40, 41, 21))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_10.setGeometry(QtCore.QRect(180, 80, 41, 21))
        self.lineEdit_10.setObjectName("lineEdit_10")

        self.retranslateUi(SettingsPanel)
        QtCore.QMetaObject.connectSlotsByName(SettingsPanel)

    def retranslateUi(self, SettingsPanel):
        _translate = QtCore.QCoreApplication.translate
        SettingsPanel.setWindowTitle(_translate("SettingsPanel", "Settings"))
        self.label.setText(_translate("SettingsPanel", "Thresholds"))
        self.label_2.setText(_translate("SettingsPanel", "SSN"))
        self.label_3.setText(_translate("SettingsPanel", "Email"))
        self.label_4.setText(_translate("SettingsPanel", "Phone"))
        self.label_5.setText(_translate("SettingsPanel", "Person"))
        self.label_6.setText(_translate("SettingsPanel", "Credit Card"))
        self.label_7.setText(_translate("SettingsPanel", "Date Of Birth"))
        self.label_9.setText(_translate("SettingsPanel", "Output Location"))
        self.label_10.setText(_translate("SettingsPanel", "Logging Location"))
        self.label_15.setText(_translate("SettingsPanel", "Logging and Output Locations"))
        self.label_16.setText(_translate("SettingsPanel", "Batch Size and Merge Gap"))
        self.label_11.setText(_translate("SettingsPanel", "Batch Size"))
        self.label_12.setText(_translate("SettingsPanel", "Merge Gap"))

class PopUpForWarning(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(397, 219)
        self.setWindowTitle("Warning")
        self.WarningLabel = QLabel(self)
        self.WarningLabel.setObjectName("WarningLabel")
        self.WarningLabel.setGeometry(10, 10, 381, 111)
    
        self.OkayButton = QPushButton(self)
        self.OkayButton.setObjectName("OkayButton")
        self.OkayButton.setGeometry(148, 153, 91, 41)
        self.OkayButton.setText("Okay")
        self.OkayButton.clicked.connect(self.close)

    def setText(self,text):
        self.WarningLabel.setText(text)


class MainWindow(QMainWindow, Ui_Form, QObject):
    def __init__(self):
        super().__init__()

        self.popUpWindow = None

        self.fileLocation = None
        
        #TODO: Lets open the settings panel first. 

        #TODO: Need to create a dictionary specifying all settings within the settings panel.

        #TODO: If the user has specified an output directory, make it so, if not it stays in the installation directory.

        # if os.path.isdir(self.cfg["output"]["path"]) is not True:
        #     self.out_dir = pathlib.Path(self.cfg["output"]["path"])
        #     self.out_dir.mkdir(parents=True, exist_ok=True)
        
            
        # if os.path.isdir(self.cfg["logging"]["path"]) is not True:
        #     os.makedirs(self.cfg["logging"]["path"])

        # self.loggingDir = self.cfg["logging"]["path"]

        self.setupUi(self)

        self.setFixedSize(QSize(650,500))

        self.ProgressBar.setMinimum(0)
        
        self.ProgressBar.setMaximum(100)

        self.FileBrowseButton.clicked.connect(self.open_file_browser)

        self.DirectoriesBrowseButton.clicked.connect(self.open_directory_browser)


        self.ScanFilesButton.clicked.connect(lambda: self.SwitchToFilePanel(2))

        self.ScanDirectoryButton.clicked.connect(lambda: self.SwitchToFilePanel(1))
        
        self.FileMainMenuButton.clicked.connect(lambda: self.SwitchToMainMenuPanel(0))

        self.DirectoriesMainMenuButton.clicked.connect(lambda: self.SwitchToMainMenuPanel(0))

        # self.FileScanNowButton.clicked.connect(self.scan)

        # self.DirectoryScanNowButton.clicked.connect(self.scan)

        self.ResultsMainMenuButton.clicked.connect(self.SwitchToMainMenuPanel)
        
        self.FindingsFolderButton.clicked.connect(lambda: self.open_external_document(self.fileLocation))

        self.FileSettingsMenu.clicked.connect(self.open_settings)

        
    def open_settings(self):
        self.settingsPanel = Ui_SettingsPanel()
        
    
    def open_file_browser(self):
        fileName = QFileDialog.getOpenFileName(self, "Find Files..", os.getcwd(), "Text Files (*.txt);;Word Files (*.docx);;PDF Files(*.pdf)")
        
        self.FileLineEdit.setText(fileName[0])
        
    def open_directory_browser(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.DirectoryLineEdit.setText(directory)

    def SwitchToFilePanel(self, index):
        self.stackedWidget.setCurrentIndex(index)
    
    def SwitchToFilePanel_Scan(self, index, scan):
        self.ProgressBar.setValue(0)
        self.stackedWidget.setCurrentIndex(index)
        scan()
    
    def SwitchToMainMenuPanel(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.FileLineEdit.setText("")
        self.DirectoryLineEdit.setText("")
        self.FileResults.setText("")
    
    def open_external_document(self, fileName):
        startfile(fileName)

    # def scan(self):
    #     try:
    #         pattern = "^(.+[/\\\\])?([^/\\\\]+)$"
    #         if re.match(pattern, self.FileLineEdit.text()) or re.match(pattern, self.DirectoryLineEdit.text()):
                
                
    #             self.stackedWidget.setCurrentIndex(3)

    #             model = PiiModel(
    #                 model_dir=self.cfg.get("model_dir", "model"),
    #                 thresholds=self.cfg.get("thresholds", {}),
    #                 batch_size=self.cfg.get("batch_size", 8),
    #             )
        
    #             self.ProgressBar.setValue(25)

    #             #Build File List 
    #             paths = []
    #             if len(self.FileLineEdit.text()) > 0:
    #                 os.path.isfile(self.FileLineEdit.text())
    #                 if os.path.isfile(self.FileLineEdit.text()):
    #                     paths.append(self.FileLineEdit.text())
    #             elif len(self.DirectoryLineEdit.text()) > 0:
    #                 if os.path.isdir(self.DirectoryLineEdit.text()):
    #                     for root, _, files in os.walk(self.DirectoryLineEdit.text()):
    #                         if any(fnmatch.fnmatch(root, ex) for ex in self.cfg.get("exclude_globs", [])):
    #                             continue
    #                         for f in files:
    #                             paths.append(os.path.join(root, f))
        
    #             self.ProgressBar.setValue(50)

    #             merged = []
    #             if paths:
    #                 for p in paths:
    #                     text = read_any(p)
    #                     if not text:
    #                         continue
    #                     findings = model.predict(text)
    #                     file_merged = merge_findings(findings, max_gap=self.cfg.get("merge_gap", 0))
    #                     fname = pathlib.Path(p).name
    #                     for f in file_merged:
    #                         merged.append({**f, "file": fname})

    #             self.ProgressBar.setValue(75)

    #             if merged:
    #                 record = {
    #                     "ts": time.time(),
    #                     "files": [pathlib.Path(p).name for p in paths],
    #                     "findings": merged,
    #                 }

    #                 with open(str(self.outputDir + os.path.sep + (pathlib.Path(p).name + ".json")), "w") as file:
    #                     file.write(json.dumps(record, indent=2))
    #                     self.FileResults.setText(json.dumps(record, indent=2))

    #                     self.fileLocation = self.outputDir + os.path.sep + (pathlib.Path(p).name + ".json")
                            
    #                     file.close()
    #                     self.ProgressBar.setValue(100)
    #                     self.stackedWidget.setCurrentIndex(4)          
    #             else:
    #                 self.stackedWidget.setCurrentIndex(0)
    #                 self.popUpWindow = PopUpForWarning()
    #                 self.popUpWindow.setText("This file or directory does not have any PII data!")
    #                 self.popUpWindow.show()


    
    #         else:
    #             if len(self.FileLineEdit.text()) == 0 or len(self.FileLineEdit.text()) == 0:
    #                 self.popUpWindow = PopUpForWarning()
    #                 self.popUpWindow.setText("Please make sure you have a File or Directory selected before scanning!")
    #                 self.popUpWindow.show()

    #     except Exception as E:
    #         logging.basicConfig(filename=self.cfg["logging"]["file"] + os.path.sep + str(dt.datetime.now().strftime('%y-%m-%d-Time-%H-%M')) + ".log" , filemode="a", format="%(asctime)s - %(levelname)s - %(message)s" )
    #         self.logger = logging.getLogger(__name__)
        
    #         self.logger.error("%s", E, exc_info=True)
            
