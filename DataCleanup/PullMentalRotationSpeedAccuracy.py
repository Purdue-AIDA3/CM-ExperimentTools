import os
import pandas as pd

# Function to calculate performance score for each trial
def calculate_mental_rotation_performance(df):
    df['Performance Score'] = 0
    
    for index, row in df.iterrows():
        if row[4] == 1:  # Correct
            df.at[index, 'Performance Score'] = max(0, 1 - row[3] / 1000)  # Score based on response time
        elif row[4] == 2:  # Error
            df.at[index, 'Performance Score'] = 0
        elif row[4] == 3:  # Too slow
            df.at[index, 'Performance Score'] = max(0, (1 - row[3] / 1000) * 0.2)  # Penalize for being too slow
    
    return df

# Function to calculate speed, accuracy, and throughput for Mental Rotation Task
def calculate_mental_rotation_metrics(response_times, statuses):
    """
    Calculates:
    - Mean Response Time (Speed)
    - Accuracy (% of correct trials)
    - Weighted Accuracy (penalizing slow trials)
    - Throughput (Speed * Accuracy)
    """

    num_trials = len(response_times)
    if num_trials == 0:
        return None, None, None, None  # Handle empty cases

    try:
        # Convert values to numeric, skipping NaNs
        response_times = [float(rt) for rt in response_times if pd.notna(rt)]
        statuses = [int(s) for s in statuses if pd.notna(s)]

        # Speed Metric (Mean RT)
        mean_rt = sum(response_times) / len(response_times) if response_times else 0

        # Accuracy Metrics
        correct_trials = statuses.count(1)
        too_slow_trials = statuses.count(3)

        accuracy = (correct_trials / num_trials) * 100  # % Correct
        weighted_accuracy = ((correct_trials + 0.5 * too_slow_trials) / num_trials) * 100  # Penalize slow

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

                    # Check if the MentalRotation or MentalRotation_table sheet exists
                    sheet_name = None
                    if 'MentalRotation' in workbook.sheet_names:
                        sheet_name = 'MentalRotation'
                    elif 'MentalRotation_table' in workbook.sheet_names:
                        sheet_name = 'MentalRotation_table'

                    if sheet_name:
                        print(f"Found {sheet_name} sheet in {workbook_path}")

                        # Read the MentalRotation sheet into a DataFrame without headers
                        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine='openpyxl')

                        # Ensure necessary columns exist
                        if df.shape[1] < 5:
                            print(f"Skipping {participant_id}: {sheet_name} does not have enough columns.")
                            continue

                        # Calculate performance score for each trial
                        df = calculate_mental_rotation_performance(df)

                        # Calculate the average performance score for the participant
                        avg_score = df['Performance Score'].mean() * 1000  # Scale to match other metrics

                        # Extract relevant data for metrics
                        statuses = df[4].astype(int, errors='ignore').tolist()
                        response_times = df[3].astype(float, errors='ignore').tolist()

                        # Calculate speed, accuracy, and throughput
                        mean_rt, accuracy, weighted_accuracy, throughput = calculate_mental_rotation_metrics(response_times, statuses)

                        if mean_rt is not None:
                            participant_data.append((participant_id, avg_score, mean_rt, accuracy, weighted_accuracy, throughput))
                            print(f"Processed {participant_id}: Avg Score = {avg_score:.2f}, Speed = {mean_rt:.2f} ms, Accuracy = {accuracy:.2f}%, Throughput = {throughput:.2f}")

                    else:
                        print(f"MentalRotation or MentalRotation_table sheet not found in {workbook_path}")

                except Exception as e:
                    print(f"Error processing file: {workbook_path}")
                    print(f"Error message: {e}")

# Create a DataFrame to store the results
results_df = pd.DataFrame(participant_data, columns=["Participant ID", "Avg Performance Score", "Mean RT (ms)", "Accuracy (%)", "Weighted Accuracy (%)", "Throughput"])
results_file = "participant_mental_rotation_metrics.xlsx"
results_df.to_excel(results_file, index=False)

# Identify and save missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

missing_file = "missing_mental_rotation_participants.txt"
with open(missing_file, "w") as f:
    for participant in missing_participants:
        f.write(participant + "\n")

# Summary Output
print("\nProcessing Complete!")
print(f"The results have been saved to {results_file}.")
print(f"Missing participant IDs have been logged in {missing_file}.")
