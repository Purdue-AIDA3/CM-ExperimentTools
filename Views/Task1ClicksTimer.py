import sys
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from .ImageWidget import ImageWidget
from Controllers.User import current_user
from .errors import save_errors
from pathlib import Path
import json

class Task1ClicksTimer(QMainWindow):
    def __init__(self, file_name, w, h, controller, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task 1")
        self.file_name = file_name
        self.controller = controller
        self.timer_expired = False  # Flag to prevent multiple calls to next_page()
        self.init_ui(w, h, pixmap)

    def init_ui(self, w, h, pixmap):
        # Main central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Image widget for the task
        self.image_label = ImageWidget(self.controller)
        self.image_label.setPixmap(pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.image_label.setStyleSheet('background-color: black')

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.image_label)

        # Control buttons
        controlLayout = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.next_page)
        self.playbutton.setEnabled(False)

        controlLayout.addWidget(self.playbutton)
        controlLayout.addWidget(self.nextButton)
        main_layout.addLayout(controlLayout)

        # Timer label
        self.timer_label = QLabel("15", self)
        self.timer_label.setFont(QFont("Arial", 24))
        self.timer_label.setStyleSheet("color: red; background-color: transparent;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setGeometry(50, 50, 100, 50)

        # Flashing light
        self.light_label = QLabel(self)
        self.light_label.setGeometry(50, 110, 150, 30)
        self.light_label.setStyleSheet('background-color: white;')
        self.light_label.setText('Warning!!!')
        self.light_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.light_label.setVisible(True)

        # Countdown timer
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer)
        self.time_left = 15

        # Flashing light timer
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.flash_light)

        # Start timers
        self.countdown_timer.start(1000)
        self.flash_timer.start(450)

    def update_timer(self):
        """Update the countdown timer and handle its expiration visually."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(str(self.time_left))
        elif self.time_left == 0:
            self.time_left -= 1  # Prevent further calls
            self.countdown_timer.stop()
            self.flash_timer.stop()
            print("DEBUG: Timer expired, but no longer affecting page transition.")

    def flash_light(self):
        # Toggle the flashing light
        current_color = self.light_label.styleSheet()
        new_color = 'background-color: red;' if 'white' in current_color else 'background-color: white;'
        self.light_label.setStyleSheet(new_color)

    def calculate_and_save_errors(self):
        # Paths for ground truth and experiment data
        base_dir = Path(__file__).resolve().parent.parent
        ground_truth_dir = base_dir / 'ground_truth'
        gt_file = ground_truth_dir / f"{self.file_name}.json"
        exp_file = Path(current_user.clicks_path) / f"{self.file_name}.json"
        output_file_dir = Path(current_user.data_path) / "position_angle_error_details"
        output_file = output_file_dir / f"{self.file_name}_errors.json"

        # Ensure directories exist
        output_file_dir.mkdir(parents=True, exist_ok=True)

        # Verify file existence
        if not gt_file.exists():
            print(f"Error: Ground truth file not found at {gt_file}")
            return

        # Calculate errors and save
        save_errors(str(gt_file), str(exp_file), str(output_file))
        print(f"DEBUG: Error data saved to {output_file}")

    def next_page(self):
        """Proceed to the next page regardless of the timer state."""
        try:
            # Save the user's click data
            self.controller.save_data()

            # Calculate and save errors
            self.calculate_and_save_errors()

            # Proceed to the next page
            if hasattr(self.parent(), 'next_page'):
                self.parent().next_page()  # Calls the next_page method in the parent (controller)
                print("DEBUG: Transitioning to the next page.")
            else:
                print("DEBUG: Parent does not have next_page method.")

        except Exception as e:
            print(f"DEBUG: An error occurred in next_page for Task1ClicksTimer: {str(e)}")



