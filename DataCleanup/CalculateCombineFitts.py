import os
import pandas as pd

# Function to calculate performance score for Fitts Law test
def calculate_fitts_law_performance(predicted_times, actual_times, statuses):
    total_score = 0
    num_trials = len(predicted_times)
    
    for i in range(num_trials):
        predicted_time = predicted_times[i]
        actual_time = actual_times[i]
        status = statuses[i]
        
        if status == 1:  # Correct
            score = (max(0, 1 - abs(predicted_time - actual_time) / predicted_time))*1000
        elif status == 2:  # Error
            score = 0
        elif status == 3:  # Too slow
            score = (max(0, 1 - abs(predicted_time - actual_time) / predicted_time) * 0.2)*1000
        
        total_score += score
    
    overall_performance_score = total_score / num_trials
    return overall_performance_score

# Directory containing participant folders
base_dir = "F:/"

# List to store average scores for each participant
participant_scores = []

# List to store all participant IDs
all_participants = []

# Iterate over each participant folder
for participant_id in os.listdir(base_dir):
    if os.path.isdir(os.path.join(base_dir, participant_id)):
        all_participants.append(participant_id)
        participant_folder = os.path.join(base_dir, participant_id, "Cognitive_tasks")
        
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
                    
                    # Check if the FittsLaw or FittsLaw_table sheet exists
                    sheet_name = None
                    if 'FittsLaw' in workbook.sheet_names:
                        sheet_name = 'FittsLaw'
                    elif 'FittsLaw_table' in workbook.sheet_names:
                        sheet_name = 'FittsLaw_table'
                    
                    if sheet_name:
                        print(f"Found {sheet_name} sheet in {workbook_path}")
                        
                        # Read the FittsLaw sheet into a DataFrame without headers
                        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine='openpyxl')
                        
                        # Extract the relevant columns (E, F, G are columns 4, 5, 6 in zero-indexed DataFrame)
                        predicted_times = df[4].tolist()
                        actual_times = df[5].tolist()
                        statuses = df[6].tolist()
                        
                        # Calculate the average performance score for the participant
                        avg_score = calculate_fitts_law_performance(predicted_times, actual_times, statuses)
                        
                        # Store the participant ID and their average score
                        participant_scores.append((participant_id, avg_score))
                        print(f"Processed {participant_id}: Average Score = {avg_score}")
                    else:
                        print(f"FittsLaw or FittsLaw_table sheet not found in {workbook_path}")
                
                except Exception as e:
                    print(f"Error processing file: {workbook_path}")
                    print(f"Error message: {e}")

# Create a DataFrame to store the results
results_df = pd.DataFrame(participant_scores, columns=["Participant ID", "Average Score"])

# Save the results to a new spreadsheet
results_df.to_excel("participant_average_fitts_law_scores.xlsx", index=False)

# Identify missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

print("Missing Participants:")
for participant in missing_participants:
    print(participant)

print("The average scores for each participant have been saved to 'participant_average_fitts_law_scores.xlsx'.")