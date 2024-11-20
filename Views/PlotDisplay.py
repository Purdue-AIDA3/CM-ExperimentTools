import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pathlib import Path
from Controllers.User import current_user


class PlotDisplay(QWidget):
    def __init__(self, file_name, next_page_callback, parent=None):
        super().__init__(parent)
        self.file_name = file_name
        self.next_page_callback = next_page_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Define path for the JSON file with error data
        json_file_path = Path(current_user.data_path) / "position_angle_error_details" / f"{self.file_name}_errors.json"

        # Load data from JSON file
        if not json_file_path.exists():
            print(f"Error: JSON file not found at {json_file_path}")
            return

        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Extract ground truths and subject guesses
        ground_truths = data.get("best_ground_truth_match", [])
        subject_guesses = data.get("subject_guesses", [])
        number_of_missed_aircrafts = data.get("number_of_missed_aircrafts", [])

        # DEBUG: Check for empty ground truths or guesses
        if not ground_truths:
            print(f"DEBUG: No ground truths found in {json_file_path}.")
        if not subject_guesses:
            print(f"DEBUG: No subject guesses found in {json_file_path}.")

        # Calculate accuracy score
        if len(subject_guesses) == 0 or all((guess[0][0] == 0 and guess[0][1] == 0) for guess in subject_guesses):
            # No valid guesses
            weighted_accuracy_score = 0.0
        else:
            # Calculate maximum possible errors
            max_positional_error = len(ground_truths) * math.sqrt(3840**2 + 2160**2)
            max_angular_error = len(ground_truths) * 180

            # Extract error metrics from JSON
            sum_of_l2_norm = data.get("sum_of_l2", 0)
            sum_of_angle_errors = data.get("abs_sum_of_angles_diff", 0)

            # Define weights for positional and angular errors
            weight_positional = 0.8
            weight_angular = 0.2

            # Calculate normalized errors
            normalized_positional_error = sum_of_l2_norm / max_positional_error
            normalized_angular_error = sum_of_angle_errors / max_angular_error

            # Compute weighted accuracy score
            weighted_accuracy_score = max(0, 100 * (1 - (weight_positional * normalized_positional_error) -
                                                    (weight_angular * normalized_angular_error)))

        # Set up the matplotlib figure and canvas
        fig, ax = plt.subplots()
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Ground Truth vs User Input')

        # Invert the Y-axis to match screen coordinates
        ax.invert_yaxis()

        # Set fixed axis limits to match 4K resolution
        #ax.set_xlim(0, 3840)
        #ax.set_ylim(0, 2160)
        ax.set_aspect('equal', adjustable='box')

        # Add accuracy score at the top of the plot
        metric_text = (f"Accuracy Score of Identified Aircraft: {weighted_accuracy_score:.2f}%\n"
                    f"Missed Aircraft: {number_of_missed_aircrafts: .2f}")
        ax.text(0.5, 1.05, metric_text, transform=ax.transAxes, fontsize=12,
                ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))

        # Continue with plotting logic...
        colors = list(mcolors.TABLEAU_COLORS.keys())
        unmatched_guesses = set(range(len(subject_guesses)))

        for i in range(len(ground_truths)):
            color_index = i % len(colors)
            ground_truth_color = mcolors.TABLEAU_COLORS[colors[color_index]]
            subject_guess_color = mcolors.to_rgba(ground_truth_color, alpha=0.5)

            # Plot ground truth location and heading
            plot_aircraft(ax, ground_truths[i], ground_truth_color, label='Ground Truth' if i == 0 else "")

            # Plot user guesses
            if i < len(subject_guesses):
                plot_aircraft(ax, subject_guesses[i], subject_guess_color, label='User Guess' if i == 0 else "")
                unmatched_guesses.discard(i)
            else:
                ax.plot(ground_truths[i][0][0], ground_truths[i][0][1], 'o', color='red', markersize=6,
                        label='Missing Guess' if i == 0 else "")
                print(f"DEBUG: Missing guess for ground truth index {i}: {ground_truths[i]}.")

        for idx in unmatched_guesses:
            if idx < len(subject_guesses):
                plot_aircraft(ax, subject_guesses[idx], "grey", label="Extra Guess" if idx == next(iter(unmatched_guesses), -1) else "")
                print(f"DEBUG: Extra guess detected at index {idx}: {subject_guesses[idx]}.")

        # Add legend to the plot
        ax.legend(loc='lower right', fontsize=10, frameon=True, title="Legend")

        # Embed the plot in the PyQt widget
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Add "Next" button to move to the following page
        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.next_page)
        layout.addWidget(next_button)

    def next_page(self):
        """Move to the next page by calling the provided callback."""
        self.next_page_callback()


def plot_aircraft(ax, aircraft_pair, color, label=None):
    """Plot an aircraft's location and heading."""
    try:
        location, heading = aircraft_pair
        # Plot the location as a circular marker
        ax.plot(location[0], location[1], marker='o', color=color, label=label)

        # Plot the heading as an arrow or line from location to heading
        ax.arrow(location[0], location[1], heading[0] - location[0], heading[1] - location[1],
                 head_width=10, head_length=10, fc=color, ec=color, alpha=1)
    except Exception as e:
        print(f"DEBUG: Error plotting aircraft: {aircraft_pair}. Error: {e}")