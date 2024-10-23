import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QSizePolicy, QGraphicsView, QStackedLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QPixmap
from .ImageWidget import ImageWidget
import time

class Task1Clicks(QWidget):

    def __init__(self, file_name, w, h, controller, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task 1")
        self.file_name = file_name
        self.controller = controller
        self.init_ui(w, h, pixmap)

    def init_ui(self, w, h, pixmap):

        self.image_label = ImageWidget(self.controller)
        self.image_label.setPixmap(pixmap.scaled(w,h, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.image_label.setStyleSheet('background-color: black')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)

        controlLayout = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.nextButton = QPushButton("Next")
        
        self.nextButton.clicked.connect(self.next_page)
        self.playbutton.setEnabled(False)

        controlLayout.addWidget(self.playbutton)
        controlLayout.addWidget(self.nextButton)
        
        self.layout.addLayout(controlLayout)

        self.setLayout(self.layout)


    def next_page(self):
        self.controller.save_data()
        self.parent().next_page()


