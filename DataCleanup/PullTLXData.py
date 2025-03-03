import os
import pandas as pd

def calculate_tlx_averages(file_path):
    """Calculate average TLX scores in sets of 10 from the TLX_Data sheet."""
    try:
        xls = pd.ExcelFile(file_path)
        if 'TLX_Data' not in xls.sheet_names:
            print(f"Warning: 'TLX_Data' sheet not found in {file_path}. Skipping file.")
            return None
        
        df = pd.read_excel(xls, sheet_name='TLX_Data', usecols='E:J')
        df.replace('null', pd.NA, inplace=True)
        
        # Print column names for debugging
        print(f"Processing {file_path}, columns found: {df.columns.tolist()}")
        
        # Mapping actual column names to desired output names
        column_mapping = {
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How mentally demanding was the task?": "Mental Demand",
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How physically demanding was the task?": "Physical Demand",
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How hurried or rushed was the pace of the task?": "Temporal Demand",
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How successful were you in accomplishing what you were asked to do?": "Performance",
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How hard did you have to work to accomplish your level of performance?": "Effort",
            "Considering the task you just completed, please indicate on the scale from Very Low (1) to Very High (20): - How insecure, discouraged, irritated, stressed, and annoyed were you?": "Frustration"
        }
        
        df = df.rename(columns=column_mapping)
        
        averages = {f"{col}_Set{i+1}": [] for i in range(3) for col in column_mapping.values()}
        
        for i, start in enumerate(range(0, len(df), 10)):
            subset = df.iloc[start:start+10]
            if not subset.isna().all().all():
                for col in column_mapping.values():
                    if col in subset.columns:
                        averages[f"{col}_Set{i+1}"].append(subset[col].mean())
        
        return {key: val[0] if val else None for key, val in averages.items()}
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def process_all_users(data_directory, output_file):
    """Iterate through user folders, process TLX data, and save results."""
    results = []
    
    for user_folder in os.listdir(data_directory):
        user_path = os.path.join(data_directory, user_folder)
        if os.path.isdir(user_path):
            # Identify the correct file format
            expected_filename = f"{user_folder}_Data_By_Time.xlsx"
            file_path = os.path.join(user_path, expected_filename)
            
            if os.path.exists(file_path):
                tlx_averages = calculate_tlx_averages(file_path)
                
                user_data = {"User": user_folder}
                if tlx_averages:
                    user_data.update(tlx_averages)
                
                results.append(user_data)
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Processed {len(results)} users. Results saved to {output_file}")

# Example usage:
data_directory = "F:\\"  # Update with actual directory path
output_file = "Participant_tlx_summary.csv"
process_all_users(data_directory, output_file)
