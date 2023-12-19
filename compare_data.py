# Import pandas library
import pandas as pd

# Read the two excel files
df1 = pd.read_excel("file1.xlsx")
df2 = pd.read_excel("file2.xlsx")

# Compare the values in the two dataframes
comparison_values = df1.values == df2.values

# Find the rows and columns where the values are different
rows, cols = np.where(comparison_values == False)

# Create a new dataframe to store the merged data
df3 = df1.copy()

# Loop through the cells that are different and update the values in df3
# Use a format like "value1 --> value2" to show the changes
for item in zip(rows, cols):
    df3.iloc[item[0], item[1]] = "{} --> {}".format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])

# Save the merged dataframe as a new excel file
df3.to_excel("file3.xlsx")
