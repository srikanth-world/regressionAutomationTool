# Import pandas and openpyxl libraries
import pandas as pd
import openpyxl

# Read the two excel files and store them in dataframes
df1 = pd.read_excel("file1.xlsx")
df2 = pd.read_excel("file2.xlsx")

# Find the differences between the two dataframes
diff = df1.compare(df2, keep_equal=True)

# Create a new dataframe to store the full data from file1 and file2
df3 = pd.concat([df1, df2], ignore_index=True)

# Load the new dataframe as a workbook object
wb = openpyxl.Workbook()
ws = wb.active

# Write the dataframe to the workbook
for r in dataframe_to_rows(df3, index=False, header=True):
    ws.append(r)

# Define a style for highlighting the cells
highlight = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

# Loop through the differences and apply the highlight style to the corresponding cells in the workbook
for row in diff.index:
    for col in diff.columns:
        cell = ws.cell(row=row+2, column=col+1)
        cell.fill = highlight

# Save the workbook as a new file
wb.save("file3.xlsx")
