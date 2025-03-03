import json
import os
import numpy as np

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def find_best_position_match(gt_points, exp_points):
    gt_points = np.array(gt_points)
    exp_points = np.array(exp_points)
    distances = np.linalg.norm(gt_points[:, None, :] - exp_points[None, :, :], axis=2)
    min_indices = np.argmin(distances, axis=1)
    min_distances = distances[np.arange(len(gt_points)), min_indices]
    best_matches = exp_points[min_indices].tolist()
    return min_distances, best_matches

def compute_angle(p1, p2):
    return np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0])) % 360

def compute_errors(gt_file, exp_file, output_file):
    try:
        gt_data = load_json(gt_file)
        exp_data = load_json(exp_file)

        gt_points = [(p['x'], p['y']) for p in gt_data['saved_points']]
        exp_points = [(p['x'], p['y']) for p in exp_data['saved_points']]

        l2_norms, best_matches = find_best_position_match(gt_points, exp_points)

        subject_guesses = [exp_points[i:i + 2] for i in range(0, len(exp_points), 2)]
        gt_pairs = [gt_points[i:i + 2] for i in range(0, len(gt_points), 2)]
        match_pairs = [best_matches[i:i + 2] for i in range(0, len(best_matches), 2)]

        gt_angles = [compute_angle(*pair) for pair in gt_pairs if len(pair) == 2]
        subject_angles = [compute_angle(*pair) for pair in subject_guesses if len(pair) == 2]
        angle_errors = [s - g for g, s in zip(gt_angles, subject_angles)]

        output_data = {
            "ground_truths": gt_pairs,
            "best_ground_truth_match": match_pairs,
            "subject_guesses": subject_guesses,
            "l2_norms": l2_norms.tolist(),
            "sum_of_l2": float(np.sum(l2_norms)),
            "gt_angles": gt_angles,
            "subject_angles": subject_angles,
            "angle_errors": angle_errors,
            "abs_sum_of_angles_diff": float(np.sum(np.abs(angle_errors))),
            "number_of_missed_aircrafts": max(0, len(gt_points) - len(exp_points)),
            "missed_aircrafts": []
        }

        save_json(output_file, output_data)
        print(f"Errors successfully saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    gt_file = r"C:\"
    exp_file = r"C:\"
    output_file = r"C:\errors.json"
    compute_errors(gt_file, exp_file, output_file)
