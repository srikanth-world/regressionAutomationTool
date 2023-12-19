import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Read the two excel files and store them in dataframes
df1 = pd.read_excel("file1.xlsx")
df2 = pd.read_excel("file2.xlsx")

# Align DataFrames based on columns and indexes
df1, df2 = df1.align(df2, axis=1, join='outer')
df1, df2 = df1.align(df2, axis=0, join='outer')

# Find the differences between the two dataframes
diff = df1.compare(df2, keep_equal=True)

# Create a new dataframe to store the full data from file1 and file2
df3 = pd.concat([df1.astype(str), df2.astype(str)], ignore_index=True)

# Load the new dataframe as a workbook object
wb = openpyxl.Workbook()
ws = wb.active

# Write the dataframe to the workbook
for r in dataframe_to_rows(df3, index=False, header=True):
    ws.append([str(cell) for cell in r])

# Define a style for highlighting the cells
highlight = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

# Loop through the differences and apply the highlight style to the corresponding cells in the workbook
for idx, (row, col) in enumerate(diff.index):
    try:
        cell = ws.cell(row=idx + 2, column=int(col) + 1)
        cell.fill = highlight
    except ValueError:
        print(f"Skipping invalid index: row={row}, col={col}")

# Save the workbook as a new file
wb.save("file3.xlsx")
