import os
import pandas as pd

# Function to calculate a more strenuous performance score for each trial
def calculate_strenuous_nback_performance(df):
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
    
    return df

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
                    
                    # Check if the NBackTask sheet exists
                    if 'NBackTask' in workbook.sheet_names:
                        print(f"Found NBackTask sheet in {workbook_path}")
                        
                        # Read the NBackTask sheet into a DataFrame without headers
                        df = pd.read_excel(workbook_path, sheet_name='NBackTask', header=None, engine='openpyxl')
                        
                        # Calculate strenuous performance score for each trial
                        df = calculate_strenuous_nback_performance(df)
                        
                        # Calculate the average strenuous performance score for the participant
                        avg_score = df['Strenuous Performance Score'].mean()*1000
                        
                        # Store the participant ID and their average score
                        participant_scores.append((participant_id, avg_score))
                        print(f"Processed {participant_id}: Average Strenuous Score = {avg_score}")
                    else:
                        print(f"NBackTask sheet not found in {workbook_path}")
                
                except Exception as e:
                    print(f"Error processing file: {workbook_path}")
                    print(f"Error message: {e}")

# Create a DataFrame to store the results
results_df = pd.DataFrame(participant_scores, columns=["Participant ID", "Average Strenuous Score"])

# Save the results to a new spreadsheet
results_df.to_excel("participant_average_strenuous_nback_scores.xlsx", index=False)

# Identify missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

print("Missing Participants:")
for participant in missing_participants:
    print(participant)

print("The average strenuous scores for each participant have been saved to 'participant_average_strenuous_nback_scores.xlsx'.")