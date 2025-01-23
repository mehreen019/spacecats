import pandas as pd

# Read the CSV file with NA handling
df = pd.read_csv('places_results.csv', na_values=['', 'null', 'NULL'], keep_default_na=True)

# Fill NA values with "N/A"
df = df.fillna("N/A")

# Count total rows before removing duplicates
initial_count = len(df)

# Remove duplicate entries based on all columns
df_cleaned = df.drop_duplicates()

# Count rows after removing duplicates
final_count = len(df_cleaned)

# Calculate number of duplicates removed
duplicates_removed = initial_count - final_count

print(f"Initial number of entries: {initial_count}")
print(f"Number of duplicates removed: {duplicates_removed}")
print(f"Final number of entries: {final_count}")

# Save the cleaned data back to CSV
df_cleaned.to_csv('places_results.csv', index=False)
print("Cleaned data saved back to places_results.csv")
