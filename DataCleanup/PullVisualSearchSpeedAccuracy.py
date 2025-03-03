import os
import pandas as pd

# Function to calculate accuracy with corrected "too slow" handling
def calculate_visual_search_metrics(response_times, statuses, distractors):
    """
    Calculates:
    - Mean Response Time (Speed)
    - Adjusted Accuracy (Handles 'too slow' responses correctly)
    - Weighted Accuracy (Penalizing slow trials incorrectly)
    - Throughput (Speed * Accuracy)
    """

    num_trials = len(response_times)
    if num_trials == 0:
        return None, None, None, None  # Handle empty cases

    try:
        # Convert values to numeric, skipping NaNs
        response_times = [float(rt) for rt in response_times if pd.notna(rt)]
        statuses = [int(s) for s in statuses if pd.notna(s)]
        distractors = [int(d) for d in distractors if pd.notna(d)]

        # Speed Metric (Mean RT)
        mean_rt = sum(response_times) / len(response_times) if response_times else 0

        # Correctly count accuracy
        correct_trials = sum(
            (distractors[i] == 1 and statuses[i] == 1) or  # Responded correctly to a distractor
            (distractors[i] == 0 and statuses[i] == 3)  # Correctly withheld response (no distractor)
            for i in range(num_trials)
        )

        # Incorrect trials (false positives or missed responses)
        incorrect_trials = sum(
            (distractors[i] == 1 and statuses[i] == 3) or  # Missed response when distractor was present
            (distractors[i] == 0 and statuses[i] == 1)  # False positive (pressed when no distractor)
            for i in range(num_trials)
        )

        # Too slow trials count
        too_slow_trials = statuses.count(3)

        # Adjusted Accuracy
        accuracy = (correct_trials / num_trials) * 100  # % Correct (handling too slow properly)
        weighted_accuracy = ((correct_trials + 0.5 * too_slow_trials) / num_trials) * 100  # Penalizing slow

        # Speed Score (Inverse RT, scaled for readability)
        speed_score = 1000 / mean_rt if mean_rt > 0 else 0

        # Throughput = Accuracy * Speed Score
        throughput = accuracy * speed_score

        return mean_rt, accuracy, weighted_accuracy, throughput

    except Exception as e:
        print(f"Error in calculating metrics: {e}")
        return None, None, None, None


# Directory containing participant folders
base_dir = "F:/"

# Lists to store metrics
participant_data = []
all_participants = []

# Iterate over each participant folder
for participant_id in os.listdir(base_dir):
    participant_path = os.path.join(base_dir, participant_id)

    if os.path.isdir(participant_path):
        all_participants.append(participant_id)
        participant_folder = os.path.join(participant_path, "Cognitive_tasks")

        # Check for both possible file names
        workbook_paths = [
            os.path.join(participant_folder, "combined_workbook.xlsx"),
            os.path.join(participant_folder, "CognitiveTaskData.xlsx")
        ]

        for workbook_path in workbook_paths:
            print(f"Processing file: {workbook_path}")
            
            if os.path.exists(workbook_path):
                try:
                    # Load the workbook
                    workbook = pd.ExcelFile(workbook_path, engine='openpyxl')

                    # Check if the VisualSearch or VisualSearch_table sheet exists
                    sheet_name = None
                    if 'VisualSearch' in workbook.sheet_names:
                        sheet_name = 'VisualSearch'
                    elif 'VisualSearch_table' in workbook.sheet_names:
                        sheet_name = 'VisualSearch_table'

                    if sheet_name:
                        print(f"Found {sheet_name} sheet in {workbook_path}")

                        # Read the VisualSearch sheet into a DataFrame without headers
                        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine='openpyxl')

                        # Ensure necessary columns exist
                        if df.shape[1] < 6:
                            print(f"Skipping {participant_id}: {sheet_name} does not have enough columns.")
                            continue

                        # Extract relevant data for metrics
                        distractors = df[2].astype(int, errors='ignore').tolist()
                        statuses = df[4].astype(int, errors='ignore').tolist()
                        response_times = df[5].astype(float, errors='ignore').tolist()

                        # Calculate speed, accuracy, and throughput with new accuracy logic
                        mean_rt, accuracy, weighted_accuracy, throughput = calculate_visual_search_metrics(
                            response_times, statuses, distractors
                        )

                        if mean_rt is not None:
                            participant_data.append((participant_id, mean_rt, accuracy, weighted_accuracy, throughput))
                            print(f"Processed {participant_id}: Speed = {mean_rt:.2f} ms, Accuracy = {accuracy:.2f}%, Throughput = {throughput:.2f}")

                    else:
                        print(f"VisualSearch or VisualSearch_table sheet not found in {workbook_path}")

                except Exception as e:
                    print(f"Error processing file: {workbook_path}")
                    print(f"Error message: {e}")

# Create a DataFrame to store the results
results_df = pd.DataFrame(participant_data, columns=["Participant ID", "Mean RT (ms)", "Accuracy (%)", "Weighted Accuracy (%)", "Throughput"])
results_file = "participant_visual_search_metrics.xlsx"
results_df.to_excel(results_file, index=False)

# Identify and save missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

missing_file = "missing_visual_search_participants.txt"
with open(missing_file, "w") as f:
    for participant in missing_participants:
        f.write(participant + "\n")

# Summary Output
print("\nProcessing Complete!")
print(f"The results have been saved to {results_file}.")
print(f"Missing participant IDs have been logged in {missing_file}.")
