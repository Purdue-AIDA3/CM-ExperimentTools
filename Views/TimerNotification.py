import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Controllers.User import current_user

class TimerNotification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('TimerNotification')
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)  # Add some spacing between widgets
    
        # Title label
        title_label = QLabel(f'The final 10 videos will continue the requirement of saying a verb for every noun provided. \nThere will now also be a 15 second timer and flashing warning light.', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Login button
        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_page)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),0,0)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum),1,0, 4,1)
        layout.addWidget(title_label, 2, 1,1,1)
        layout.addWidget(self.next_button, 5, 1,1,1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum),1,2, 4,1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 6, 0)

        self.setLayout(layout)

    def next_page(self):
        self.parent().next_page()
