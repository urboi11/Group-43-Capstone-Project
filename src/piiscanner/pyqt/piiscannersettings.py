from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QDoubleSpinBox, QSpinBox, QFileDialog
import platform

##TODO: Add Tool Tips to each LineEdit to signify what type of text is needed.
class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(15)
        self.setFixedSize(662, 420)

        self.thresholdsLabel = QtWidgets.QLabel(self)        
        self.thresholdsLabel.setGeometry(QtCore.QRect(20, 40, 101, 41))
        self.thresholdsLabel.setText("Thresholds:")
        self.thresholdsLabel.setFont(self.font1)

        #SSN Label and LineEdit.
        self.ssnLabel = QtWidgets.QLabel(self)
        self.ssnLabel.setGeometry(QtCore.QRect(30, 85, 101, 41))
        self.ssnLabel.setFont(self.font1)
        self.ssnLabel.setText("SSN:")

        self.double_spin_box_ssn = QDoubleSpinBox(self)

        self.double_spin_box_ssn.setRange(0.0, 0.9)  # Min and Max values
        self.double_spin_box_ssn.setSingleStep(0.1)    # Amount to change per click
        self.double_spin_box_ssn.setDecimals(1)        # Number of decimal places shown
        self.double_spin_box_ssn.setGeometry(QtCore.QRect(130, 95, 71, 21))  
        self.double_spin_box_ssn.setValue(0.8)
    
    
        #Email Label and Spin Box

        self.emailLabel = QtWidgets.QLabel(self)
        self.emailLabel.setGeometry(QtCore.QRect(30, 125, 101, 41))
        self.emailLabel.setFont(self.font1)
        self.emailLabel.setText("Email:")

        self.double_spin_box_email = QDoubleSpinBox(self)

        self.double_spin_box_email.setRange(0.0, 0.9)
        self.double_spin_box_email.setSingleStep(0.1)
        self.double_spin_box_email.setDecimals(1)        
        self.double_spin_box_email.setGeometry(QtCore.QRect(130, 135, 71, 21))
        self.double_spin_box_email.setValue(0.6)

        #Phone Label and Spin Box
        
        self.phoneLabel = QtWidgets.QLabel(self)
        self.phoneLabel.setGeometry(QtCore.QRect(30, 165, 101, 41))
        self.phoneLabel.setFont(self.font1)
        self.phoneLabel.setText("Phone:")

        self.double_spin_box_phone = QDoubleSpinBox(self)

        self.double_spin_box_phone.setRange(0.0, 0.9)
        self.double_spin_box_phone.setSingleStep(0.1)  
        self.double_spin_box_phone.setDecimals(1)   
        self.double_spin_box_phone.setGeometry(QtCore.QRect(130, 175, 71, 21))
        self.double_spin_box_phone.setValue(0.6)


        #Person Label and LineEdit

        self.personLabel = QtWidgets.QLabel(self)
        self.personLabel.setGeometry(QtCore.QRect(30, 200, 101, 41))
        self.personLabel.setFont(self.font1)
        self.personLabel.setText("Person:")

        self.double_spin_box_person = QDoubleSpinBox(self)

        self.double_spin_box_person.setRange(0.0, 0.9)
        self.double_spin_box_person.setSingleStep(0.1)     
        self.double_spin_box_person.setDecimals(1)
        self.double_spin_box_person.setGeometry(QtCore.QRect(130, 210, 71, 21))
        self.double_spin_box_person.setValue(0.7)
        #Credit Card Label and LineEdit

        self.cardLabel = QtWidgets.QLabel(self)
        self.cardLabel.setGeometry(QtCore.QRect(30, 235, 101, 41))
        self.cardLabel.setFont(self.font1)
        self.cardLabel.setText("Credit Card:")

        self.double_spin_box_card = QDoubleSpinBox(self)

        self.double_spin_box_card.setGeometry(QtCore.QRect(130, 245, 71, 21))
        self.double_spin_box_card.setRange(0.0, 0.9)
        self.double_spin_box_card.setSingleStep(0.1)   
        self.double_spin_box_card.setDecimals(1)
        self.double_spin_box_card.setValue(0.8)
        
        #Date Of Birth Label and LineEdit


        self.dobLabel = QtWidgets.QLabel(self)
        self.dobLabel.setGeometry(QtCore.QRect(30, 265, 101, 41))
        self.dobLabel.setFont(self.font1)
        self.dobLabel.setText("Date Of Birth:")

        self.double_spin_box_dob = QDoubleSpinBox(self)

        self.double_spin_box_dob.setGeometry(QtCore.QRect(130, 275, 71, 21))
        self.double_spin_box_dob.setRange(0.0, 0.9)
        self.double_spin_box_dob.setSingleStep(0.1) 
        self.double_spin_box_dob.setDecimals(1)
        self.double_spin_box_dob.setValue(0.6)   


        #Ip Address Label and Double Spin Box.
        self.IPAddressLabel = QtWidgets.QLabel(self)
        self.IPAddressLabel.setGeometry(QtCore.QRect(30, 295, 101, 41))
        self.IPAddressLabel.setFont(self.font1)
        self.IPAddressLabel.setText("IP Address: ")

        self.double_spin_box_ip_address = QDoubleSpinBox(self)
        self.double_spin_box_ip_address.setGeometry(QtCore.QRect(130, 305, 71, 21))
        self.double_spin_box_ip_address.setRange(0.0, 0.9)
        self.double_spin_box_ip_address.setSingleStep(0.1)
        self.double_spin_box_ip_address.setDecimals(1)   
        self.double_spin_box_ip_address.setValue(0.6)

        #Address Label and Double Spin Box.
        self.addressLabel = QtWidgets.QLabel(self)
        self.addressLabel.setGeometry(QtCore.QRect(30, 325, 101, 41))
        self.addressLabel.setFont(self.font1)
        self.addressLabel.setText("Address: ")

        self.double_spin_box_address = QDoubleSpinBox(self)
        self.double_spin_box_address.setGeometry(QtCore.QRect(130, 335, 71, 21))
        self.double_spin_box_address.setRange(0.0, 0.9)
        self.double_spin_box_address.setSingleStep(0.1)
        self.double_spin_box_address.setDecimals(1)   
        self.double_spin_box_address.setValue(0.6)

        #TODO: Add Input validation for Output Location and Logging Location.
        
        # Output Location Label and LineEdit
        self.outputLabel = QtWidgets.QLabel(self)
        self.outputLabel.setGeometry(QtCore.QRect(275, 40, 115, 41))
        self.outputLabel.setFont(self.font1)
        self.outputLabel.setText("Output Location:")

        self.outputLineEdit = QtWidgets.QLineEdit(self)
        self.outputLineEdit.setGeometry(QtCore.QRect(405, 50, 130, 21))

        self.outputButton = QtWidgets.QPushButton(self)
        self.outputButton.setGeometry(QtCore.QRect(550, 45, 90, 30))
        self.outputButton.setFont(self.font1)
        self.outputButton.setText("Browse")

        self.outputButton.clicked.connect(self.open_directory_browser_output)

        #Logging Label and Line Edit
        self.loggingLabel = QtWidgets.QLabel(self)
        self.loggingLabel.setGeometry(QtCore.QRect(275, 75, 120, 41))
        self.loggingLabel.setFont(self.font1)
        self.loggingLabel.setText("Logging Location:")

        self.loggingLineEdit = QtWidgets.QLineEdit(self)
        self.loggingLineEdit.setGeometry(QtCore.QRect(405, 90, 130, 21))

        self.loggingButton = QtWidgets.QPushButton(self)
        self.loggingButton.setGeometry(QtCore.QRect(550, 85, 90, 30))
        self.loggingButton.setFont(self.font1)
        self.loggingButton.setText("Browse")

        self.loggingButton.clicked.connect(self.open_directory_browser_logging)


        #Batch Size Label and Line Edit
        self.batchSizeLabel = QtWidgets.QLabel(self)
        self.batchSizeLabel.setGeometry(QtCore.QRect(275, 115, 120, 41))
        self.batchSizeLabel.setFont(self.font1)
        self.batchSizeLabel.setText("Batch Size:")

        self.spin_box_batch_size = QSpinBox(self)
        self.spin_box_batch_size.setGeometry(QtCore.QRect(465, 130, 71, 21))
        self.spin_box_batch_size.setRange(0, 8)
        self.spin_box_batch_size.setSingleStep(1)
        self.spin_box_batch_size.setValue(8)


        # #Merge Gap Label and Line Edit

        self.mergeGapLabel = QtWidgets.QLabel(self)
        self.mergeGapLabel.setGeometry(QtCore.QRect(275, 155, 120, 41))
        self.mergeGapLabel.setFont(self.font1)
        self.mergeGapLabel.setText("Merge Gap:")

        self.spin_box_merge_gap = QSpinBox(self)
        self.spin_box_merge_gap.setGeometry(QtCore.QRect(465, 170, 71, 21))
        self.spin_box_merge_gap.setRange(0, 2)
        self.spin_box_merge_gap.setSingleStep(1)
        self.spin_box_merge_gap.setValue(2)
        

        #Okay and Exit Button

        self.okayButton = QtWidgets.QPushButton(self)
        self.okayButton.setGeometry(QtCore.QRect(200, 360, 90, 30))
        self.okayButton.setFont(self.font1)
        self.okayButton.setText("Save")
        self.okayButton.clicked.connect(self.save_settings)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(QtCore.QRect(350, 360, 90, 30))
        self.exitButton.setFont(self.font1)
        self.exitButton.setText("Exit")
        self.exitButton.clicked.connect(self.reset_values)

        #Init base values for settings.
        self.ssnValue = 0.0

        self.emailValue = 0.0

        self.phoneValue = 0.0

        self.personValue = 0.0

        self.cardValue = 0.0

        self.dobValue = 0.0

        self.IPAddressValue = 0.0

        self.addressValue = 0.0

        self.outputLocation = ""

        self.loggingLocation = ""

        self.batchSizeValue = 0

        self.mergeGapValue = 0

    def reset_values(self):

        if self.ssnValue != 0.0:
            pass
        else:
            self.ssnValue = 0.0
            self.double_spin_box_ssn.setValue(0.8)

        if self.emailValue != 0.0:
            pass
        else:
            self.emailValue = 0.0
            self.double_spin_box_email.setValue(0.6)

        if self.phoneValue != 0.0:
            pass
        else:
            self.phoneValue = 0.0
            self.double_spin_box_phone.setValue(0.6)

        if self.personValue != 0.0:
            pass
        else:
            self.personValue = 0.0
            self.double_spin_box_person.setValue(0.7)

        if self.cardValue != 0.0:
            pass
        else:
            self.cardValue = 0.0
            self.double_spin_box_card.setValue(0.8)

        if self.dobValue != 0.0:
            pass
        else:
            self.dobValue = 0.0
            self.double_spin_box_dob.setValue(0.6)

        if self.IPAddressValue != 0.0:
            pass
        else:
            self.IPAddressValue = 0.0
            self.double_spin_box_ip_address.setValue(0.6)

        if self.addressValue != 0.0:
            pass
        else:
            self.addressValue = 0.0
            self.double_spin_box_address.setValue(0.6)

        if self.outputLocation != "":
            pass
        else:
            self.outputLocation = ""
            self.outputLineEdit.setText("")

        if self.loggingLocation != "":
            pass
        else:
            self.loggingLocation = ""
            self.loggingLineEdit.setText("")

        if self.batchSizeValue != 0:
            pass
        else:
            self.batchSizeValue = 0
            self.spin_box_batch_size.setValue(8)

        if self.mergeGapValue != 0:
            pass
        else:
            self.mergeGapValue = 0
            self.spin_box_merge_gap.setValue(2)

        self.close()

    def save_settings(self):

        self.ssnValue = self.double_spin_box_ssn.text()

        self.emailValue = self.double_spin_box_email.text()

        self.phoneValue = self.double_spin_box_phone.text()

        self.personValue = self.double_spin_box_person.text()

        self.cardValue = self.double_spin_box_card.text()

        self.dobValue = self.double_spin_box_dob.text()

        self.IPAddressValue = self.double_spin_box_ip_address.text()

        self.addressValue = self.double_spin_box_address.text()

        self.outputLocation = self.outputLineEdit.text()

        self.loggingLocation = self.loggingLineEdit.text()

        self.batchSizeValue = self.spin_box_batch_size.text()

        self.mergeGapValue = self.spin_box_batch_size.text()

        self.close()

    def open_directory_browser_output(self):
        if platform.system() == "Darwin":
            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            self.outputLineEdit.setText(directory)

        if platform.system() == "Windows":
            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")).replace("/", "\\") + "\\"
            self.outputLineEdit.setText(directory)


    def open_directory_browser_logging(self):
        if platform.system() == "Darwin":
            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            self.loggingLineEdit.setText(directory)

        if platform.system() == "Windows":
            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")).replace("/", "\\") + "\\"
            self.loggingLineEdit.setText(directory)
