from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Instructions(QWidget):
    def __init__(self, instructions, parent=None, image=None):
        super().__init__(parent)

        self.setWindowTitle("Instructions")

        self.init_ui(instructions, image)
    

    def init_ui(self, instructions, image):
        layout = QVBoxLayout()

        title_label = QLabel(f'Instructions', self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        instruction_label = QLabel(instructions)
        instruction_label.setFont(QFont("Arial", 14))
        instruction_label.setWordWrap(True)
        layout.addWidget(instruction_label)
        if image != None:
            pixmap = QPixmap(image)  
            if not pixmap.isNull():
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(image_label)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def next_page(self):
        self.parent().next_page()
