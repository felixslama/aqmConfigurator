from .model import MainModel
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QLabel
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
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.submitInput)
        self.aboutButton = QPushButton("About")
        self.aboutButton.clicked.connect(self.showCredits)
        self.urlLabel = QLabel(self)
        self.urlLabel.setText('URL:')
        self.urlInput = QLineEdit(self)
        self.tokenLabel = QLabel(self)
        self.tokenLabel.setText('Token:')
        self.tokenInput = QLineEdit(self)
        inputLayout = QVBoxLayout()
        inputLayout.addStretch()
        inputLayout.addWidget(self.urlLabel)
        inputLayout.addWidget(self.urlInput)
        inputLayout.addWidget(self.tokenLabel)
        inputLayout.addWidget(self.tokenInput)
        inputLayout.addWidget(self.submitButton)
        inputLayout.addStretch()
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buildButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.aboutButton)
        self.layout.addLayout(inputLayout)
        self.layout.addLayout(buttonLayout)

    def buildRelease(self):
        self.main.build()

    def submitInput(self):
        if self.tokenInput.text().isdigit():
            self.main.submit(self.urlInput.text(), self.tokenInput.text())
        else:
            QMessageBox.critical(self, "Error", "Token has to be numeric!")

    def showCredits(self):
        text = f"<center>"\
        "<h1>AQM-Configurator</h1>"\
        "<p>Configurator and Builder</p>"\
        "<p>Copyright &copy; f1re & k1f0</p>"\
        "</center>"
        QMessageBox.about(self, "About", text)
        # was enabled for debugging/testing
        #self.main.createCert()
    
    def downloadLatest(self):
        self.main.download()
