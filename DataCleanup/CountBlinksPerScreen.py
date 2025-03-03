import pandas as pd

def count_id_x_occurrences(file_path, sheet_name="Sheet1", output_path="output.xlsx"):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert timestamps to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors='coerce')
    df["End Time_x"] = pd.to_datetime(df["End Time_x"], errors='coerce')
    
    # Extract relevant columns and drop rows with missing values in Screen_x
    df_filtered = df[["Screen_x", "Start Time", "End Time_x", "id_x"]].dropna(subset=["Screen_x"])
    
    # Initialize a dictionary to store counts
    screen_counts = {}
    
    # Iterate through each screen entry and count occurrences of id_x within the time range
    for _, row in df_filtered.iterrows():
        screen_name = row["Screen_x"]
        start_time = row["Start Time"]
        end_time = row["End Time_x"]
        
        # Count occurrences where id_x falls within the time range
        count = df[(df["id_x"].notna()) & (df["Start Time"] >= start_time) & (df["Start Time"] <= end_time)]["id_x"].count()
        
        # Store count
        screen_counts[screen_name] = screen_counts.get(screen_name, 0) + count
    
    # Convert result to a DataFrame
    screen_counts_df = pd.DataFrame(screen_counts.items(), columns=["Screen_x", "id_x Count"])
    
    # Save to an Excel file
    #screen_counts_df.to_excel(output_path, index=False)
    screen_counts_df.to_excel(output_path, index=False, engine='openpyxl')

    return screen_counts_df

# Example usage
file_path = "F:\\Combined_Data_By_Time.xlsx"  # Update with the correct file path
output_path = "F:\\BlinksCount.xlsx"  # Update with desired output file name
result_df = count_id_x_occurrences(file_path, output_path=output_path)
print(f"Results saved to {output_path}")
