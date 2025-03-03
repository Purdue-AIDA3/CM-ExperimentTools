import pandas as pd
import os
import json

# Directory containing JSON files
directory = 'F:\\position_angle_error_details'

# List to hold data from all files
data_list = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
             # Add the filename to the data at the beginning
            data = {'filename': filename, **data}
            data_list.append(data)

# Combine all data into a single DataFrame
df = pd.json_normalize(data_list)

# Save DataFrame to a CSV file in the same directory
output_file_path = os.path.join(directory, 'combined_data.csv')
df.to_csv(output_file_path, index=False)

print(f"Combined data has been saved to {output_file_path}")