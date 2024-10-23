import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class Break(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
    
    def init_ui(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_remaining = 5 * 60
        self.timer.start(1000)

        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.next_button = QPushButton("Next")

        self.next_button.clicked.connect(self.next_page)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.next_button)
        self.setLayout(layout)

        self.update_timer()

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.setText(f"Time Remaining: {time_str}")
        self.time_remaining -= 1
        if self.time_remaining < 0:
            self.timer.stop()

    def next_page(self):
        self.parent().next_page()
