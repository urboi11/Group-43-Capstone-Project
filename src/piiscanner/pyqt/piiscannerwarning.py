from PySide6.QtWidgets import QWidget, QLabel, QPushButton


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