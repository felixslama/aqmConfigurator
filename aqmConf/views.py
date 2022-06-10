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
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.input_layout = QHBoxLayout()
        self.setWindowTitle("aqmConfigurator")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)
        self.main = MainModel()
        self.setup_UI()

    def setup_UI(self):
        self.build_button = QPushButton("Build")
        self.build_button.clicked.connect(self.build_release)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_input)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_credits)
        self.token_label = QLabel(self)
        self.token_label.setText('OTP-Token:')
        self.token_input = QLineEdit(self)
        self.input_layout.addStretch()
        self.input_layout.addWidget(self.token_label)
        self.input_layout.addWidget(self.token_input)
        self.input_layout.addWidget(self.submit_button)
        self.input_layout.addStretch()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.build_button)
        self.button_layout.addWidget(self.about_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)

    def build_release(self):
        self.main.build()

    def submit_input(self):
        if self.token_input.text().isdigit():
            submitRes = self.main.submit(self.token_input.text())
            if submitRes:
                QMessageBox.information(self, "Success", "Credentials received!")
            else:
                QMessageBox.critical(self, "Error", "Token invalid or expired!")
        else:
            QMessageBox.critical(self, "Error", "Token has to be numeric!")

    def show_credits(self):
        text = f"<center>"\
        "<h1>AQM-Configurator</h1>"\
        "<p>Configurator and Builder</p>"\
        "<p>Copyright &copy; f1re & k1f0</p>"\
        "</center>"
        QMessageBox.about(self, "About", text)

    def download_latest(self):
        self.main.download()
