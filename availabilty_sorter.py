###Annotates individuals input file by number of available blocks, can later be sorted using Excel

import pandas as pd

# Load the CSV file
file_path = '/mnt/data/Individual Application Fall 2024.csv'
df = pd.read_csv(file_path)

# Identify columns that have "Availability" in their name
availability_columns = [col for col in df.columns if 'Availability' in col]

# Define a function to count the number of entries in availability columns
def count_availability_entries(row):
    total_entries = 0
    for col in availability_columns:
        if pd.notna(row[col]):
            total_entries += len(row[col].split(','))
    return total_entries

# Create a new column that sums the number of entries for each row
df['Total Availability Entries'] = df.apply(count_availability_entries, axis=1)

# Display the updated dataframe with the new column (optional for viewing purposes)
import ace_tools as tools; tools.display_dataframe_to_user(name="Updated Availability Data", dataframe=df)
