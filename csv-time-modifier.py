#Pads blocks by adding 25 minutes to start time and assuming the class is 1 hour long,
#also adds 25 minutes to end time. Assumption is not necessarily correct for classes
#less than an hour

import pandas as pd
from datetime import datetime, timedelta

# Load the provided CSV file
file_path = '/Users/aptitude/Desktop/VSVS_project/modified inputs/FINALEDIT teachers.csv'  # Replace with the actual file path
df = pd.read_csv(file_path)

# Function to subtract 25 minutes from the original start time
def subtract_25_minutes(time_str):
    if pd.isna(time_str):
        return time_str  # Return NaN as is
    try:
        time_obj = datetime.strptime(time_str, '%I:%M:%S %p')
        updated_time = time_obj - timedelta(minutes=25)
        return updated_time.strftime('%I:%M:%S %p')
    except ValueError:
        return time_str  # In case of unexpected formats, return the original

# Function to set the end time to 1 hour and 50 minutes after the new start time
def add_1_hour_50_minutes_to_new_start(start_time_str):
    if pd.isna(start_time_str):
        return start_time_str  # Return NaN as is
    try:
        time_obj = datetime.strptime(start_time_str, '%I:%M:%S %p')
        updated_end_time = time_obj + timedelta(hours=1, minutes=50)
        return updated_end_time.strftime('%I:%M:%S %p')
    except ValueError:
        return start_time_str  # In case of unexpected formats, return the original

# List of columns with start and end times
time_columns = [col for col in df.columns if "Start Time" in col or "End Time" in col]

# Applying the functions to start and end time columns
for col in time_columns:
    if "Start Time" in col:
        df[col] = df[col].apply(subtract_25_minutes)
    elif "End Time" in col:
        corresponding_start_col = col.replace("End Time", "Start Time")
        df[col] = df[corresponding_start_col].apply(add_1_hour_50_minutes_to_new_start)

# Save the updated dataframe to a new CSV
output_path = 'TEACHERTIMES_PLUS_25.csv'  # Replace with desired output path
df.to_csv(output_path, index=False)

print(f"Updated file saved at: {output_path}")
