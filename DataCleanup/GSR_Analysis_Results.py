import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_prominences

def analyze_gsr(file_path, resistance_column, output_path="gsr_analysis_output.xlsx"):
    # Load the GSR data from multiple sheets
    excel_sheets = pd.ExcelFile(file_path).sheet_names
    print("Available sheets:", excel_sheets)
    
    df_windows_sheet = [s for s in excel_sheets if 'window' in s.lower()]
    df_gsr_sheet = [s for s in excel_sheets if 'gsr' in s.lower()]
    
    if not df_windows_sheet or not df_gsr_sheet:
        print("Error: Could not find sheets containing 'window' or 'gsr'. Check sheet names.")
        return
    
    df_windows = pd.read_excel(file_path, sheet_name=df_windows_sheet[0])
    df_gsr = pd.read_excel(file_path, sheet_name=df_gsr_sheet[0])
    
    # Convert timestamps to datetime
    df_windows['Start Time'] = pd.to_datetime(df_windows['Start Time'], errors='coerce')
    df_windows['End Time'] = pd.to_datetime(df_windows['End Time'], errors='coerce')
    df_gsr['Start Time'] = pd.to_datetime(df_gsr['Start Time'], errors='coerce')
    
    # Ensure the resistance column exists
    if resistance_column not in df_gsr.columns:
        print(f"Column '{resistance_column}' not found in the dataset.")
        return
    
    # Convert resistance column to numeric
    df_gsr[resistance_column] = pd.to_numeric(df_gsr[resistance_column], errors='coerce')
    
    # Preserve timestamps even when GSR values are missing
    timestamps = df_gsr['Start Time'].values
    gsr_values = df_gsr[resistance_column].values
    
    # Ensure there are enough valid data points for analysis
    if np.count_nonzero(~np.isnan(gsr_values)) < 3:
        print("Not enough valid GSR data points for analysis.")
        return
    
    # Adjust window size dynamically
    window_size = min(10, len(gsr_values[~np.isnan(gsr_values)]))  # Reduce if not enough points
    
    # Smooth the data using a moving average filter
    smoothed_gsr = np.convolve(np.nan_to_num(gsr_values), np.ones(window_size)/window_size, mode='valid')
    smoothed_timestamps = timestamps[:len(smoothed_gsr)]
    
    # Detect peaks
    if len(smoothed_gsr) == 0:
        print("No valid GSR data after smoothing.")
        return
    
    peaks, _ = find_peaks(smoothed_gsr, height=np.percentile(smoothed_gsr, 75), distance=20)
    prominences = peak_prominences(smoothed_gsr, peaks)[0]
    
    # Establish a baseline (rolling median)
    baseline = pd.Series(smoothed_gsr).rolling(window=min(50, len(smoothed_gsr)), min_periods=1).median()
    
    # Compute peak amplitudes relative to baseline
    peak_amplitudes = smoothed_gsr[peaks] - baseline.iloc[peaks].values
    
    # Assign screens based on the active screen during each peak
    peak_screens = []
    for peak_time in smoothed_timestamps[peaks]:
        matching_rows = df_windows.loc[(df_windows['Start Time'] <= peak_time) & (df_windows['End Time'] >= peak_time)]
        if not matching_rows.empty:
            peak_screens.append(matching_rows.iloc[0]['Screen'])
        else:
            peak_screens.append("Unknown")
    
    # Save results to Excel
    results_df = pd.DataFrame({
        'Timestamp': smoothed_timestamps[peaks],
        'Screen': peak_screens,
        'Peak Value': smoothed_gsr[peaks],
        'Baseline Value': baseline.iloc[peaks].values,
        'Amplitude Change': peak_amplitudes,
        'Prominence': prominences
    })
    results_df.to_excel(output_path, index=False, engine='openpyxl')
    
    # Plot the data with screen windows
    plt.figure(figsize=(16, 8))
    plt.plot(smoothed_timestamps, smoothed_gsr, label='Smoothed GSR', color='blue', alpha=0.7)
    plt.plot(smoothed_timestamps, baseline, label='Baseline', linestyle='dashed', color='orange')
    plt.scatter(smoothed_timestamps[peaks], smoothed_gsr[peaks], color='red', label='Peaks', zorder=3)
    
    # Highlight screen intervals and add screen labels
    for _, row in df_windows.iterrows():
        if pd.notna(row['Start Time']) and pd.notna(row['End Time']):
            plt.axvspan(row['Start Time'], row['End Time'], color='gray', alpha=0.3)
            plt.text(row['Start Time'], max(smoothed_gsr), row['Screen'], rotation=90, verticalalignment='bottom', fontsize=8)
    
    plt.xlabel('Time')
    plt.ylabel('GSR Resistance')
    plt.title('GSR Resistance Analysis with Peak Detection and Screen Intervals')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Results saved to {output_path}")
    return results_df

# Example usage
file_path = "F:\\"  # Update with your file
resistance_column = "Shimmer_A5F3_GSR_CAL"  # Update with your column name
output_path = "gsr_analysis_results.xlsx"  # Output file
analyze_gsr(file_path, resistance_column, output_path)
