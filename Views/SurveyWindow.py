import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Controllers.User import current_user

class SurveyWindow(QWidget):
    def __init__(self, survey_id, parent=None, metadata=None):
        super().__init__(parent)
        self.setWindowTitle('Survey')
        self.init_ui(survey_id, metadata)

    def init_ui(self, survey_id, metadata):
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Add some spacing between widgets

       
        self.webview = QWebEngineView()
        self.webview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.webview)
        self.url = f"https://purdue.ca1.qualtrics.com/jfe/form/{survey_id}?userid={current_user.uid}"
        if metadata != None:
            for key,value in metadata.items():
                self.url += f"&{key}={value}"
        self.webview.load(QUrl(self.url))
        self.webview.urlChanged.connect(self.next_page)

        self.setLayout(layout)

    def next_page(self, url):
        if not url.toString().startswith(self.url):
            self.parent().next_page()

