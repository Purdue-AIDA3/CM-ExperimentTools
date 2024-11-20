import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import json
from pathlib import Path
from Controllers.User import current_user  # To access current user data paths

def plot_ground_truth_vs_user_input(gt_points, exp_points, best_gt, best_exp):
    """
    Plots ground truth and user input trajectories.
    
    Parameters
    ----------
    gt_points : numpy array
        Ground truth data.
    exp_points : numpy array
        User guess data.
    best_gt : numpy array
        Matched ground truth data.
    best_exp : numpy array
        Matched user guesses.
    """
    # Debugging: Print values to be plotted
    print("DEBUG: Plotting ground truth trajectories:", gt_points.tolist())
    print("DEBUG: Plotting user guess trajectories:", exp_points.tolist())
    print("DEBUG: Matched ground truth:", best_gt.tolist())
    print("DEBUG: Matched user guesses:", best_exp.tolist())

    fig, ax = plt.subplots()
    ax.set_title("Ground Truth vs User Guesses")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    # Plot ground truth
    for i, trajectory in enumerate(gt_points):
        x_coords = [trajectory[0][0], trajectory[1][0]]
        y_coords = [trajectory[0][1], trajectory[1][1]]
        ax.plot(x_coords, y_coords, label=f"Ground Truth {i+1}", color="blue")

    # Plot user guesses
    for i, trajectory in enumerate(exp_points):
        x_coords = [trajectory[0][0], trajectory[1][0]]
        y_coords = [trajectory[0][1], trajectory[1][1]]
        ax.plot(x_coords, y_coords, label=f"User Guess {i+1}", color="red")

    ax.legend()
    plt.show()


def plot_points_and_trajectories(ax, points, color, label=None):
    """Plot points and connecting lines for a given set of coordinates."""
    for i in range(0, len(points), 4):
        x = [points[i], points[i+2]]
        y = [points[i+1], points[i+3]]
        ax.plot(x[0], y[0], marker='o', color=color) # Plot the first point as a circle
        ax.plot(x[1], y[1], marker='^', color=color) # Plot the second point as a triangle
        ax.plot(x, y, color=color) # Plot the connecting line between the points

# Example usage
if __name__ == "__main__":
    # Replace 'task_file_name' with the actual file name used in Task1Clicks
    file_name = "task_file_name"  # Update with the file name
    plot_ground_truth_vs_user_input(file_name)
