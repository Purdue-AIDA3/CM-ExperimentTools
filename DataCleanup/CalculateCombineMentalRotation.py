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
                        
                        # Calculate performance score for each trial
                        df = calculate_mental_rotation_performance(df)
                        
                        # Calculate the average performance score for the participant
                        avg_score = df['Performance Score'].mean()*1000
                        
                        # Store the participant ID and their average score
                        participant_scores.append((participant_id, avg_score))
                        print(f"Processed {participant_id}: Average Score = {avg_score}")
                    else:
                        print(f"MentalRotation or MentalRotation_table sheet not found in {workbook_path}")
                
                except Exception as e:
                    print(f"Error processing file: {workbook_path}")
                    print(f"Error message: {e}")

# Create a DataFrame to store the results
results_df = pd.DataFrame(participant_scores, columns=["Participant ID", "Average Score"])

# Save the results to a new spreadsheet
results_df.to_excel("participant_average_mental_rotation_scores.xlsx", index=False)

# Identify missing participants
processed_participants = results_df["Participant ID"].tolist()
missing_participants = list(set(all_participants) - set(processed_participants))

print("Missing Participants:")
for participant in missing_participants:
    print(participant)

print("The average scores for each participant have been saved to 'participant_average_mental_rotation_scores.xlsx'.")