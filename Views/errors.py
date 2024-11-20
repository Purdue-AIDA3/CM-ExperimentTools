"""
Creates the position_angle_error_details folder
"""

import glob
import json
import math
from itertools import permutations 
import numpy as np
import re
import os

def get_points_from_dict(points_dict):
    """
    function to convert dict to list

    Parameters
    ----------
    points_dict: dict
        contains dictionary of (x, y) coordinates

    Returns
    -------
    list
        returns the coordinates in the form of a list
    """
    ret = []
    for i in range(len(points_dict)):
        ret.append((points_dict[i]['x'], points_dict[i]['y']))
    return ret

def find_sum_of_errors(gt_comb, exp_comb):
    """
    Function to find sum of errors. 
    Uses l2 norm to find errors and then adds them up

    Parameters
    ----------
    gt_comb: numpy array
        contains coordinates
    exp_comb: numpy array
        contains coordinates
    
    Returns
    -------
    int
        sum of l2 norms
    numpy array
        l2 norms between ground truth data and subject data
    """
    # Replace invalid guesses (0, 0) with the ground truth positions to simulate maximum error
    invalid_guesses = (exp_comb == 0).all(axis=1)
    exp_comb[invalid_guesses] = gt_comb[invalid_guesses]

    l2_norm = np.linalg.norm(gt_comb - exp_comb, axis=1)
    return sum(l2_norm), l2_norm

def find_raw_arctan2_angles(first, second):
    """
    Find raw angle in degrees wrt. horizontal axis.

    Parameters
    ----------
    first: numpy array
        contains coordinates
    second: numpy array
    contains coordinates

    Returns
    -------
    float
        contains angles in degrees
    """
    # print(first)
    # print(second)
    diff = second - first
    # print(diff)
    return -np.rad2deg(np.arctan2((diff[1] + 0.0000001), (diff[0] + 0.0000001))) # arctan for finding angle, and rad2deg for converting to degrees.

def find_intersection(a,b,c,d):
    """
    Find intersection point between 2 lines

    Parameters
    ----------
    a, b, c, d: lists
        contains the four coordinates (2 from each line) -  one for the direction of heading of the red aircraft, another for the missed aircraft
    
    Returns
    -------
    floats
        intersection coordinates
    """
    # standard form line eq Line_AB
    a1 = b[1] - a[1]
    b1 = a[0] - b[0]
    c1 = a1*a[0] + b1*a[1]
 
    # standard form line eq Line_CD
    a2 = d[1] - c[1]
    b2 = c[0] - d[0]
    c2 = a2 * c[0] + b2 * c[1]
 
    determinant = a1 * b2 - a2 * b1
 
    if (determinant == 0):
        return math.inf, math.inf
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
    return x, y

def find_intersection_distance(red_gt, intersection_point):
    """
    Find distance from intersection point to red aircraft, and check if the intersection occurs in front of the red aircraft or behind.

    Parameters
    ----------
    red_gt: numpy array
        coordinates for the red aircraft
    
    intersection_point:
        coordinates for the intersection point
    
    Returns
    -------
    float
        distance between red aircraft and the intersection point
    """
    distance = np.linalg.norm(red_gt[0] - intersection_point)
    first_angle = find_raw_arctan2_angles(red_gt[0], red_gt[1])
    second_angle = find_raw_arctan2_angles(red_gt[0], intersection_point)
    if abs(first_angle - second_angle) < 10:                                             # if angles are similar, both points are on the same side, else no
        pass
    else:
        distance = -distance
    return distance

def get_intersection_distance_from_red_gt(red_gt, gt_left_over):
    """
    Wrapper function for intersection distance calculations.

    Parameters
    ----------
    red_gt: numpy array
        coordinates of red aircraft

    gt_leftover: numpy array
        coordinates of the missed aircraft
    
    Returns
    -------
    float
        intersection distance
    """
    intersection_point = find_intersection(red_gt[0], red_gt[1], gt_left_over[0], gt_left_over[1])
    intersection_point = np.array(intersection_point)
    # print(red_gt)
    # print(gt_left_over[i])
    intersection_distance = find_intersection_distance(red_gt, intersection_point)
    return intersection_distance

def get_distance_between_aircrafts(red_gt, gt_left_over):
    """
    Find euclidean distance from red aircraft to missed aircraft

    Parameters
    ----------
    red_gt: numpy array
        coordinates of red aircraft

    gt_leftover: numpy array
        coordinates of the missed aircraft
    
    Returns
    -------
    float
        euclidean distance
    """
    diff = red_gt - gt_left_over
    l2_norm = np.linalg.norm(diff[0])
    return l2_norm

def find_angles(arr):
    """
    Finds the angle of a vector wrt. the horizontal axis and returns it in degrees.
    
    Parameters
    ----------
    arr: numpy array
        has shape (x, 2, 2)
    
    Returns
    -------
    numpy array
        has shape (x,). Contains angles in degrees.
    
    """
    first = arr[:, 0, :]
    second = arr[:, 1, :]
    diff = second - first
    return -np.rad2deg(np.arctan2((diff[:, 1] + 0.0000001), (diff[:, 0] + 0.0000001))) # arctan for finding angle, and rad2deg for converting to degrees.

def find_angle_errors(gt, exp):
    """
    Finds angle errors by subtraction
    
    Parameters
    ----------
    gt: numpy array
        Contains ground truth data, has shape (x, 2, 2)
    exp: numpy array
        Contains subject data, has shape (x, 2, 2)
    
    Returns
    -------
    numpy array
        has shape (x,). Contains angles of vectors in ground truth
    numpy array
        has shape (x,). Contains angles of vectors in subject data
    numpy array
        has shape (x,). Contains difference in angles (max difference possible is 180).
    """
    gt_angles = find_angles(gt)
    exp_angles = find_angles(exp)

    # Ensure both arrays are >= 0
    gt_angles = np.where(gt_angles < 0, gt_angles + 360, gt_angles)
    exp_angles = np.where(exp_angles < 0, exp_angles + 360, exp_angles)

    # Pad exp_angles if it has fewer elements than gt_angles
    if len(exp_angles) < len(gt_angles):
        padding = np.ones(len(gt_angles) - len(exp_angles)) * 180  # Use 180 for max angle error
        exp_angles = np.concatenate([exp_angles, padding])

    # Calculate angle differences
    d = gt_angles - exp_angles
    d = np.where((np.abs(d) > 180) & (d > 0), d - 360, d)  # Handle large angle differences
    d = np.where((np.abs(d) > 180) & (d < 0), d + 360, d)  # Normalize angles to within -180 to 180

    return gt_angles, exp_angles, d

def find_best_position_match(gt_points, gt_positions, exp_positions):
    """
    Finds the best matches between ground truth data positions and subject data positions.

    Parameters
    ----------
    gt_points: numpy array
        Full ground truth points (including positions and headings) in shape (n, 2, 2).
    gt_positions: numpy array
        Positions (centers) of ground truth in shape (n, 2).
    exp_positions: numpy array
        Positions (centers) of user guesses in shape (m, 2).

    Returns
    -------
    best_gt: numpy array
        Matched ground truth points in shape (min(m, n), 2, 2).
    best_s: float
        Sum of L2 norms (total error).
    best_l2: numpy array
        L2 norms for each match in shape (min(m, n),).
    gt_left_over: numpy array
        Unmatched ground truth points (aircraft missed by user).
    num_not_attempted: int
        Count of unmatched ground truth points.
    """
    exp_num = len(exp_positions)
    gt_num = len(gt_positions)

    # Initialize variables
    best_s = float("inf")
    best_perm = []
    gt_left_over = []
    best_l2 = np.zeros(gt_num)

    # Edge case: if no user guesses
    if exp_num == 0:
        best_gt = gt_points
        best_exp = np.zeros_like(best_gt)
        best_l2 = np.linalg.norm(gt_positions - np.zeros_like(gt_positions), axis=1)
        return best_gt, np.sum(best_l2), best_l2, gt_points, len(gt_points)

    # Handle extra user guesses by only considering the first `gt_num` guesses for matching
    exp_positions = exp_positions[:gt_num]
    
    # Iterate through all possible permutations of ground truth assignments
    all_permutations = permutations(range(gt_num), len(exp_positions))
    for perm in all_permutations:
        perm = list(perm)
        gt_perm = gt_positions[perm]
        s, l2_norm = find_sum_of_errors(np.array(gt_perm), exp_positions)

        # Update if this permutation has a smaller error
        if s < best_s:
            best_s = s
            best_l2 = l2_norm
            best_perm = perm
            gt_left_over = list(set(range(gt_num)) - set(perm))  # Unmatched ground truth indices

    # Prepare matched ground truth and subject guesses
    best_gt = gt_points[best_perm]
    best_exp = exp_positions

    # Handle unmatched ground truth points
    if gt_left_over:
        gt_left_over = gt_points[gt_left_over]

    return best_gt, best_s, best_l2, gt_left_over, len(gt_left_over)


import numpy as np
import json

def save_errors(gt_path, exp_path, file_name_to_save):
    """
    Save errors between ground truth and subject guesses in a JSON file.

    Parameters
    ----------
    gt_path: str
        File path to the ground truth JSON data.
    exp_path: str
        File path to the subject's data JSON.
    file_name_to_save: str
        File path to save the calculated error data.
    """
    try:
        # Load ground truth data
        with open(gt_path, 'r') as f:
            gt_data = json.load(f)

        # Attempt to load experimental data, handle missing file
        try:
            with open(exp_path, 'r') as f:
                exp_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Clicks data file not found: {exp_path}. Using empty placeholder.")
            exp_data = {"saved_points": []}

        # Extract points from ground truth and experimental data
        gt_points = [tuple(pt.values()) for pt in gt_data["saved_points"]]
        exp_points = [tuple(pt.values()) for pt in exp_data.get("saved_points", [])]

        # Handle odd numbers of clicks in user guesses
        if len(exp_points) % 2 != 0:
            print("Warning: Odd number of user clicks detected. Dropping unmatched click.")
            exp_points = exp_points[:-1]

        # Group every two points into (location, heading) pairs
        gt_points = np.array([gt_points[i:i + 2] for i in range(0, len(gt_points), 2)])
        exp_points = np.array([exp_points[i:i + 2] for i in range(0, len(exp_points), 2)])

        # Separate positions (location only) for matching
        gt_positions = gt_points[:, 0]  # First point in each pair
        exp_positions = exp_points[:, 0] if len(exp_points) > 0 else np.zeros((0, 2))

        # Handle case with no user guesses
        if exp_positions.shape[0] == 0:
            print("DEBUG: No user guesses detected. Treating all ground truth as missed.")
            exp_points = np.zeros((len(gt_points), 2, 2))
            best_gt = gt_points
            best_s = 0  # No error to compute
            best_l2 = np.linalg.norm(gt_positions - np.zeros_like(gt_positions), axis=1)
            gt_left_over = gt_points
            num_not_attempted = len(gt_points)
            gt_angles = np.ones(len(gt_points)) * 180  # Maximum angle error
            exp_angles = np.ones(len(gt_points)) * 180
            angles_diff = np.ones(len(gt_points)) * 180
        else:
            # Match user guesses to ground truth
            best_gt, best_s, best_l2, gt_left_over, num_not_attempted = find_best_position_match(
                gt_points, gt_positions, exp_positions
            )

            # Ensure lengths of best_gt and exp_points match
            if len(exp_points) < len(best_gt):
                padding = np.zeros((len(best_gt) - len(exp_points), 2, 2))
                exp_points = np.concatenate((exp_points, padding))

            # Calculate angle errors
            gt_angles, exp_angles, angles_diff = find_angle_errors(best_gt, exp_points)

        # Save results to JSON
        result = {
            "ground_truths": gt_points.tolist(),
            "best_ground_truth_match": best_gt.tolist(),
            "subject_guesses": exp_points.tolist(),
            "l2_norms": best_l2.tolist(),
            "sum_of_l2": best_s,
            "gt_angles": gt_angles.tolist(),
            "subject_angles": exp_angles.tolist(),
            "angle_errors": angles_diff.tolist(),
            "abs_sum_of_angles_diff": np.sum(np.abs(angles_diff)),
            "number_of_missed_aircrafts": num_not_attempted,
            "missed_aircrafts": gt_left_over.tolist() if isinstance(gt_left_over, np.ndarray) else gt_left_over,
        }

        with open(file_name_to_save, "w", encoding='utf-8') as outfile:
            json.dump(result, outfile, separators=(',', ':'), indent=4)
        print(f"Error data saved to {file_name_to_save}")

    except Exception as e:
        print(f"Error saving errors: {e}")

if __name__ == "__main__":
    for folder in glob.glob("../../../user_data/*/"):                                   # go through all relevant folders, currently in the COVEE directory
        if re.search("\D*\d{10}", folder):
            folder_name = folder[19:-1]                                         # store folder name for later use
            print(folder)
            for file in glob.glob(folder + "/clicks_data/*.json"):            # go through all relevant files
                if re.search("\D*Task_\d_\d_\d\D*", file):
                    file_name = file[file.rfind("/") + 1:-5]                  # store file name for later use
                    # print(file_name)
                    if re.search("secondary", file_name):                      # to facilitate accessing the correct ground truth file
                        f_name = file_name[:-10]
                    else:
                        f_name = file_name
                    gt_file = "../UAV_ground_truth/" + f_name + ".json"   
                    exp_file = file
                    # file name to save data as json
                    place_to_save = "../position_angle_error_details/" + folder_name + "/"
                    if not os.path.isdir(place_to_save):
                        os.makedirs(place_to_save)   
                    file_name_to_save = place_to_save + "/" + file_name + ".json"
                    print(file_name_to_save)
                    save_errors(gt_file, exp_file, file_name_to_save)      # call wrapper function
