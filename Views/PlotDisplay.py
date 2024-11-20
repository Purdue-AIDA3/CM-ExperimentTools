import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

        # Extract ground truths and subject guesses as pairs
        ground_truths = data.get("best_ground_truth_match", [])
        subject_guesses = data.get("subject_guesses", [])

        if not ground_truths:
            print(f"DEBUG: No ground truths found in {json_file_path}.")
        if not subject_guesses:
            print(f"DEBUG: No subject guesses found in {json_file_path}.")

        # Set up the matplotlib figure and canvas for embedding in PyQt6
        fig, ax = plt.subplots()
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Ground Truth vs User Input')

        # Define colors for each aircraft's location and heading
        colors = list(mcolors.TABLEAU_COLORS.keys())

        # Track unmatched guesses for visual distinction
        unmatched_guesses = set(range(len(subject_guesses)))

        # Plot each ground truth and the closest matching user guess
        for i in range(len(ground_truths)):
            color_index = i % len(colors)
            ground_truth_color = mcolors.TABLEAU_COLORS[colors[color_index]]
            subject_guess_color = mcolors.to_rgba(ground_truth_color, alpha=0.5)

            # Plot ground truth location and heading
            plot_aircraft(ax, ground_truths[i], ground_truth_color, label='Ground Truth' if i == 0 else "")

            # Find the closest subject guess if available
            if i < len(subject_guesses):
                plot_aircraft(ax, subject_guesses[i], subject_guess_color, label='User Guess' if i == 0 else "")
                unmatched_guesses.discard(i)  # Mark this guess as matched
            else:
                # Indicate a missing guess for this ground truth point
                ax.plot(ground_truths[i][0][0], ground_truths[i][0][1], 'o', color='red', markersize=6, label='Missing Guess' if i == 0 else "")
                print(f"DEBUG: Missing guess for ground truth index {i}: {ground_truths[i]}.")

        # Plot any unmatched guesses as extra guesses
        for idx in unmatched_guesses:
            if idx < len(subject_guesses):  # Ensure the index is valid
                plot_aircraft(ax, subject_guesses[idx], "grey", label="Extra Guess" if idx == next(iter(unmatched_guesses), -1) else "")
                print(f"DEBUG: Extra guess detected at index {idx}: {subject_guesses[idx]}.")

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