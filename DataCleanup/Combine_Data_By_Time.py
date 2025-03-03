import pandas as pd

# Function to load all sheets from the workbook into DataFrames
def load_workbook(file_path):
    """
    Load all sheets from an Excel workbook into a dictionary of DataFrames.
    """
    sheets = pd.ExcelFile(file_path)
    dataframes = {sheet_name: sheets.parse(sheet_name) for sheet_name in sheets.sheet_names}
    return dataframes

# Function to standardize the time column across DataFrames
def standardize_time(df, time_column):
    """
    Standardize the time column to a consistent datetime format.
    """
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
    return df

# Function to merge all DataFrames on the time column
def merge_dataframes(dfs, time_column):
    """
    Merge a list of DataFrames on a shared time column.
    """
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=time_column, how='outer')
    return merged_df

# Main processing function
def process_workbook(file_path, output_path, time_column):
    """
    Load, clean, and align data from an Excel workbook and export the result.
    
    Parameters:
    - file_path: Path to the input Excel workbook.
    - output_path: Path to the output cleaned file.
    - time_column: The name of the time column used for merging.
    """
    print("Loading workbook...")
    dataframes = load_workbook(file_path)

    print("Standardizing time columns...")
    standardized_dfs = []
    for sheet_name, df in dataframes.items():
        if time_column in df.columns:
            print(f"Standardizing time column in sheet '{sheet_name}'...")
            df = standardize_time(df, time_column)
            standardized_dfs.append(df)
        else:
            print(f"Warning: '{time_column}' not found in sheet '{sheet_name}'")

    print("Merging sheets...")
    merged_df = merge_dataframes(standardized_dfs, time_column)

    print("Exporting cleaned data...")
    merged_df.to_excel(output_path, index=False)
    print(f"Cleaned and aligned data exported to {output_path}")

# Example usage
if __name__ == "__main__":
    # Path to the input workbook
    input_file = "F:\\9159849367\\9159849367_Data_By_Time.xlsx"

    # Path to the output cleaned file
    output_file = "F:\\9159849367\\Combined_Data_By_Time.xlsx"

    # The name of the time column to align data on
    time_column_name = "Start Time"

    # Process the workbook
    process_workbook(input_file, output_file, time_column_name)
