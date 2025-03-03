import os
import pandas as pd

# Function to calculate all performance metrics for N-back
def calculate_nback_metrics(df):
    """
    Calculates:
    - Mean Reaction Time (Speed)
    - Accuracy (% correct trials)
    - Weighted Accuracy (penalizing misses and false alarms)
    - Throughput (Speed Score * Accuracy)
    - Strenuous Performance Score (Custom scoring system)
    """
    
    num_trials = len(df)
    if num_trials == 0:
        return None, None, None, None, None  # Handle empty cases

    try:
        # Extract relevant columns
        response_times = df[7].astype(float, errors='ignore').tolist()  # Column 8 (Reaction Time)
        scores = df[3].astype(int, errors='ignore').tolist()  # Column 4 (Score: 1 = Correct, 0 = Incorrect)
        misses = df[5].astype(int, errors='ignore').tolist()  # Column 6 (Misses)
        false_alarms = df[6].astype(int, errors='ignore').tolist()  # Column 7 (False Alarms)

        # Speed Metric (Mean RT)
        mean_rt = sum(response_times) / len(response_times) if response_times else 0

        # Accuracy Metric
        correct_trials = sum(scores)  # Since Score column is 1 (correct) or 0 (incorrect)
        accuracy = (correct_trials / num_trials) * 100  # % Correct

        # Weighted Accuracy (accounting for misses and false alarms)
        weighted_accuracy = ((correct_trials - 0.5 * (sum(misses) + sum(false_alarms))) / num_trials) * 100

        # Speed Score (Inverse RT, scaled for readability)
        speed_score = 1000 / mean_rt if mean_rt > 0 else 0

        # Throughput = Accuracy * Speed Score
        throughput = accuracy * speed_score

        # Calculate Strenuous Performance Score
        df['Strenuous Performance Score'] = 0
        for index, row in df.iterrows():
            if row[2] == 1:  # Matching stimulus
                if row[4] == 1:  # Correct match
                    df.at[index, 'Strenuous Performance Score'] = 2  # Higher score for correct match
                else:  # Incorrect match
                    df.at[index, 'Strenuous Performance Score'] = -2  # Penalty for incorrect match
            else:  # Non-matching stimulus
                if row[6] == 1:  # Miss
                    df.at[index, 'Strenuous Performance Score'] = -1  # Penalty for miss
                elif row[7] == 1:  # False alarm
                    df.at[index, 'Strenuous Performance Score'] = -3  # Higher penalty for false alarm
                else:  # Correct non-match
                    df.at[index, 'Strenuous Performance Score'] = 1  # Lower score for correct non-match

        strenuous_score = df['Strenuous Performance Score'].mean() * 1000  # Scaling to match previous output format

        return mean_rt, accuracy, weighted_accuracy, throughput, strenuous_score

    except Exception as e:
        print(f"Error in calculating metrics: {e}")
        return None, None, None, None, None


# Directory containing participant folders
base_dir = "F:/"

# Lists to store metrics
nback_data = []
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

                    # Check if the NBackTask sheet exists
                    sheet_name = next((s for s in ['NBackTask', 'NBack_table'] if s in workbook.sheet_names), None)

                    if sheet_name:
                        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine='openpyxl')

                        # Ensure necessary columns exist
                        if df.shape[1] < 12:
                            print(f"Skipping {participant_id}: {sheet_name} does not have enough columns.")
                            continue

                        # Compute metrics
                        mean_rt, accuracy, weighted_accuracy, throughput, strenuous_score = calculate_nback_metrics(df)

                        if mean_rt is not None:
                            nback_data.append((participant_id, mean_rt, accuracy, weighted_accuracy, throughput, strenuous_score))
                            print(f"Processed {participant_id}: Speed = {mean_rt:.2f} ms, Accuracy = {accuracy:.2f}%, Throughput = {throughput:.2f}, Strenuous Score = {strenuous_score:.2f}")

                    else:
                        print(f"No NBackTask sheet found in {workbook_path}")

                except Exception as e:
                    print(f"Error processing {workbook_path} for {participant_id}: {e}")

# Create DataFrame of results
results_df = pd.DataFrame(nback_data, columns=["Participant ID", "Mean RT (ms)", "Accuracy (%)", "Weighted Accuracy (%)", "Throughput", "Strenuous Score"])
results_file = "participant_nback_metrics.xlsx"
results_df.to_excel(results_file, index=False)

# Identify and save missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

missing_file = "missing_nback_participants.txt"
with open(missing_file, "w") as f:
    for participant in missing_participants:
        f.write(participant + "\n")

# Summary Output
print("\nProcessing Complete!")
print(f"The results have been saved to {results_file}.")
print(f"Missing participant IDs have been logged in {missing_file}.")
