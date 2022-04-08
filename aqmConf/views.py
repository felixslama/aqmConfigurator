from .model import MainModel
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QMessageBox
)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("aqmConfigurator")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.main = MainModel()
        self.setupUI()
    
    def setupUI(self):
        self.buildButton = QPushButton("Build")
        self.buildButton.clicked.connect(self.buildRelease)
        self.checkButton = QPushButton("Check")
        self.checkButton.clicked.connect(self.checkUpdate)
        self.aboutButton = QPushButton("About")
        self.aboutButton.clicked.connect(self.showCredits)
        layout = QHBoxLayout()
        layout.addWidget(self.checkButton)
        layout.addWidget(self.buildButton)
        layout.addStretch()
        layout.addWidget(self.aboutButton)
        self.layout.addLayout(layout)
    
    def buildRelease(self):
        self.main.build()

    def checkUpdate(self):
        self.main.check()

    def showCredits(self):
        text = f"<center>"\
        "<h1>AQM-Configurator</h1>"\
        "<p>Configurator and Builder</p>"\
        "<p>Copyright &copy; k1f0</p>"\
        "</center>"
        QMessageBox.about(self, "About", text)
