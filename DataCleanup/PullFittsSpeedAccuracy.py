import os
import pandas as pd

# Function to calculate speed (Mean Response Time) and accuracy
def calculate_speed_and_accuracy(response_times, statuses):
    """
    Calculates:
    - Mean Response Time (Speed)
    - Accuracy (% of correct trials)
    - Weighted Accuracy (penalizing slow trials)
    """

    num_trials = len(response_times)
    if num_trials == 0:
        return None, None, None  # Handle empty cases

    try:
        # Convert values to numeric, skipping NaNs
        response_times = [float(rt) for rt in response_times if pd.notna(rt)]
        statuses = [int(s) for s in statuses if pd.notna(s)]

        # Speed Metric
        mean_rt = sum(response_times) / len(response_times) if response_times else 0

        # Accuracy Metrics
        correct_trials = statuses.count(1)
        error_trials = statuses.count(2)
        too_slow_trials = statuses.count(3)

        accuracy = (correct_trials / num_trials) * 100  # % Correct
        weighted_accuracy = ((correct_trials + 0.5 * too_slow_trials) / num_trials) * 100  # Penalize slow

        return mean_rt, accuracy, weighted_accuracy

    except Exception as e:
        print(f"Error in calculating metrics: {e}")
        return None, None, None


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
            if os.path.exists(workbook_path):
                try:
                    workbook = pd.ExcelFile(workbook_path, engine='openpyxl')

                    # Check for correct sheet
                    sheet_name = next((s for s in ['FittsLaw', 'FittsLaw_table'] if s in workbook.sheet_names), None)

                    if sheet_name:
                        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine='openpyxl')

                        # Ensure necessary columns exist
                        if df.shape[1] < 7:
                            print(f"Skipping {participant_id}: {sheet_name} does not have enough columns.")
                            continue

                        # Extract relevant data
                        try:
                            predicted_times = df[4].astype(float, errors='ignore').tolist()
                            actual_times = df[5].astype(float, errors='ignore').tolist()
                            statuses = df[6].astype(int, errors='ignore').tolist()

                            # Calculate metrics
                            mean_rt, accuracy, weighted_accuracy = calculate_speed_and_accuracy(actual_times, statuses)

                            if mean_rt is not None:
                                participant_data.append((participant_id, mean_rt, accuracy, weighted_accuracy))
                                print(f"Processed {participant_id}: Speed = {mean_rt:.2f} ms, Accuracy = {accuracy:.2f}%, Weighted Acc = {weighted_accuracy:.2f}%")

                        except Exception as conv_error:
                            print(f"Data conversion issue for {participant_id}: {conv_error}")
                            continue

                    else:
                        print(f"No FittsLaw sheet found in {workbook_path}")

                except Exception as e:
                    print(f"Error processing {workbook_path} for {participant_id}: {e}")

# Create DataFrame of results
results_df = pd.DataFrame(participant_data, columns=["Participant ID", "Mean RT (ms)", "Accuracy (%)", "Weighted Accuracy (%)"])
results_file = "participant_speed_accuracy.xlsx"
results_df.to_excel(results_file, index=False)

# Identify and save missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

missing_file = "missing_participants.txt"
with open(missing_file, "w") as f:
    for participant in missing_participants:
        f.write(participant + "\n")

# Summary Output
print("\nProcessing Complete!")
print(f"The results have been saved to {results_file}.")
print(f"Missing participant IDs have been logged in {missing_file}.")
