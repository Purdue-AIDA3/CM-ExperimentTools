import sys
import os
import numpy as np
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .ImageWidget import ImageWidget
from Controllers.User import current_user  # Access current user paths
from .errors import save_errors  # Import error calculation function
import json

class Task1Clicks(QWidget):

    def __init__(self, file_name, w, h, controller, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task 1")
        self.file_name = file_name
        self.controller = controller
        self.init_ui(w, h, pixmap)

    def init_ui(self, w, h, pixmap):
        self.image_label = ImageWidget(self.controller)
        self.image_label.setPixmap(pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio))
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

    def calculate_and_save_errors(self):
        # Construct path to the 'ground_truth' folder in 'research_program'
        base_dir = Path(__file__).resolve().parent.parent  # Points to 'research_program'
        ground_truth_dir = base_dir / 'ground_truth'

        # Define the ground truth file path based on task name
        gt_file = ground_truth_dir / f"{self.file_name}.json"
        exp_file = Path(current_user.clicks_path) / f"{self.file_name}.json"
        output_file_dir = Path(current_user.data_path) / "position_angle_error_details"
        output_file = output_file_dir / f"{self.file_name}_errors.json"

        # Ensure the output directory exists
        output_file_dir.mkdir(parents=True, exist_ok=True)

        # Check if ground truth file exists
        if not gt_file.exists():
            print(f"Error: Ground truth file not found at {gt_file}")
            return  # Exit the function if file is missing

        # Run error calculation and save results to JSON
        save_errors(str(gt_file), str(exp_file), str(output_file))
        print(f"Error data saved to {output_file}")

    def next_page(self):
        """Save user clicks, calculate errors, then move to the NASA-TLX survey."""
        # Save the user's click data
        self.controller.save_data()

        # Calculate and save errors
        self.calculate_and_save_errors()

        # Move to the next page (e.g., NASA-TLX survey)
        self.parent().next_page()
