import pandas as pd

def count_id_y_and_sum_duration(file_path, sheet_name="Sheet1", output_path="output.xlsx"):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert timestamps to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors='coerce')
    df["End Time_x"] = pd.to_datetime(df["End Time_x"], errors='coerce')
    
    # Extract relevant columns and drop rows with missing values in Screen_x
    df_filtered = df[["Screen_x", "Start Time", "End Time_x", "id_y", "duration_y"]].dropna(subset=["Screen_x"])
    
    # Initialize a dictionary to store counts and sums
    screen_stats = {}
    
    # Iterate through each screen entry and count occurrences of id_y and sum duration_y within the time range
    for _, row in df_filtered.iterrows():
        screen_name = row["Screen_x"]
        start_time = row["Start Time"]
        end_time = row["End Time_x"]
        
        # Filter occurrences where id_y falls within the time range
        relevant_rows = df[(df["id_y"].notna()) & (df["Start Time"] >= start_time) & (df["Start Time"] <= end_time)]
        count = relevant_rows["id_y"].count()
        duration_sum = relevant_rows["duration_y"].sum()
        
        # Store count and sum
        screen_stats[screen_name] = {"id_y Count": count, "duration_y Sum": duration_sum}
    
    # Convert result to a DataFrame
    screen_stats_df = pd.DataFrame.from_dict(screen_stats, orient="index").reset_index()
    screen_stats_df.columns = ["Screen_x", "id_y Count", "duration_y Sum"]
    
    # Save to an Excel file
    screen_stats_df.to_excel(output_path, index=False, engine='openpyxl')
    
    return screen_stats_df

# Example usage
file_path = "F:\\Combined_Data_By_Time.xlsx"  # Update with the correct file path
output_path = "F:\\Fixationscount.xlsx"  # Update with desired output file name
result_df = count_id_y_and_sum_duration(file_path, output_path=output_path)
print(f"Results saved to {output_path}")
