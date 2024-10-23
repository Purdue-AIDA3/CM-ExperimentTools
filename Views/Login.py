import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Controllers import UserController

class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Login')
        self.controller = UserController()
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)  # Add some spacing between widgets
    
        # Title label
        title_label = QLabel('Login', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Username input
        # self.username_input = QLineEdit(self)
        # self.username_input.setPlaceholderText('Username')

        # # Password input
        # self.password_input = QLineEdit(self)
        # self.password_input.setPlaceholderText('Password')
        # self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Login button
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),0,0)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum),1,0, 4,1)
        layout.addWidget(title_label, 2, 1,1,1)
        # layout.addWidget(self.username_input, 3, 1,1,1)
        # layout.addWidget(self.password_input,4,1,1,1)
        layout.addWidget(self.login_button, 5, 1,1,1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum),1,2, 4,1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 6, 0)

        self.setLayout(layout)

    def login(self):
        # username = self.username_input.text()
        # password = self.password_input.text()
        logged_in, uid = self.controller.login()
        if logged_in: 
            self.parent().next_page()
        else:
            QMessageBox.warning(self, 'Login Failed', uid)

