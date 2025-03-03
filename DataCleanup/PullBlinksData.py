import os
import pandas as pd

def calculate_blinks_per_minute(file_path):
    """Calculate blinks per minute from a given data file."""
    try:
        # Load available sheet names
        xls = pd.ExcelFile(file_path)
        if 'blinks' not in xls.sheet_names:
            print(f"Warning: 'blinks' sheet not found in {file_path}. Skipping file.")
            return 0
        
        df = pd.read_excel(xls, sheet_name='blinks')
        
        # Debugging: Print column names to verify
        print(f"Processing {file_path}, columns found: {df.columns.tolist()}")
        
        # Handle potential column name variations
        possible_columns = ["Start Time", "StartTime", "start_time", "start timestamp"]
        for col in possible_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                total_duration_minutes = (df[col].max() - df[col].min()).total_seconds() / 60
                blinks_per_minute = len(df) / total_duration_minutes if total_duration_minutes > 0 else 0
                return blinks_per_minute
        
        print(f"Warning: No recognized timestamp column found in {file_path}")
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def process_all_users(data_directory, output_file):
    """Iterate through user folders, process blinks data, and save results."""
    results = []
    
    for user_folder in os.listdir(data_directory):
        user_path = os.path.join(data_directory, user_folder)
        if os.path.isdir(user_path):
            # Identify the correct file format
            expected_filename = f"{user_folder}_Data_By_Time.xlsx"
            file_path = os.path.join(user_path, expected_filename)
            
            if os.path.exists(file_path):
                blinks_per_min = calculate_blinks_per_minute(file_path)
                results.append({"User": user_folder, "Blinks Per Minute": blinks_per_min})
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Processed {len(results)} users. Results saved to {output_file}")

# Example usage:
data_directory = "F:\\"  # Update with actual directory path
output_file = "blinks_summary.csv"
process_all_users(data_directory, output_file)
