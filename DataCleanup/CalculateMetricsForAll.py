import pandas as pd

# Ppath to the combined data spreadsheet
file_path = "C:\\combined_data.xlsx" 

# Load the data from the spreadsheet
combined_data = pd.read_excel(file_path, engine='openpyxl')

# Print the column names and first few rows to verify
print("Column names in the DataFrame:", combined_data.columns)
print("First few rows of the DataFrame:\n", combined_data.head())

# Define maximum possible L2 norm and angle difference
max_l2_norm = 3000 # Slight padding was added to account for future participants
max_angle_diff = 609.081705501152

# Define penalty for missing an aircraft
penalty_missed_aircraft = ((1500/3000)+(180/609.081705501152))

# Convert columns to numeric values if they are not already
combined_data['sum_of_l2'] = pd.to_numeric(combined_data['sum_of_l2'], errors='coerce')
combined_data['abs_sum_of_angles_diff'] = pd.to_numeric(combined_data['abs_sum_of_angles_diff'], errors='coerce')
combined_data['number_of_missed_aircrafts'] = pd.to_numeric(combined_data['number_of_missed_aircrafts'], errors='coerce')

# Function to calculate performance score for each trial
def calculate_performance_score(row):
    # Normalize L2 norm and angle difference
    normalized_l2_norm = row['sum_of_l2'] / max_l2_norm
    normalized_angle_diff = row['abs_sum_of_angles_diff'] / max_angle_diff
    
    # Convert to performance scores
    l2_score = 1 - normalized_l2_norm
    angle_score = 1 - normalized_angle_diff
    
    # Calculate penalty for missed aircrafts
    penalty = row['number_of_missed_aircrafts'] * penalty_missed_aircraft
    
    # Calculate overall performance score for the trial
    performance_score = (l2_score + angle_score - penalty)*1000
    
    return performance_score

# Apply the function to calculate performance scores for each trial
combined_data['performance_score'] = combined_data.apply(calculate_performance_score, axis=1)

# Calculate overall performance score for each participant
participant_scores = combined_data.groupby('participant_id')['performance_score'].mean().reset_index()

# Calculate performance scores for the first, second, and third sets of 10 trials in chronological order
combined_data['trial_set'] = combined_data.groupby('participant_id').cumcount() // 10 + 1

first_set_scores = combined_data[combined_data['trial_set'] == 1].groupby('participant_id')['performance_score'].mean().reset_index()
second_set_scores = combined_data[combined_data['trial_set'] == 2].groupby('participant_id')['performance_score'].mean().reset_index()
third_set_scores = combined_data[combined_data['trial_set'] == 3].groupby('participant_id')['performance_score'].mean().reset_index()

# Save the updated data with performance scores to a new Excel file
with pd.ExcelWriter('participant_performance_scores.xlsx') as writer:
    participant_scores.to_excel(writer, sheet_name='Overall_Performance', index=False)
    first_set_scores.to_excel(writer, sheet_name='First_Set_Performance', index=False)
    second_set_scores.to_excel(writer, sheet_name='Second_Set_Performance', index=False)
    third_set_scores.to_excel(writer, sheet_name='Third_Set_Performance', index=False)

print("Performance scores calculated and saved to 'participant_performance_scores.xlsx'.")