import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Read the two excel files and store them in dataframes
df1 = pd.read_excel("file1.xlsx")
df2 = pd.read_excel("file2.xlsx")

# Get the original order of columns
original_columns_order = list(df1.columns)

# Align DataFrames based on original order of columns
df1, df2 = df1.align(df2, axis=1, join='outer', fill_value=None)

# Reorder columns to match the original order
df1 = df1[original_columns_order]
df2 = df2[original_columns_order]

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
for index, row in diff.iterrows():
    for col, value in row.items():
        try:
            cell = ws.cell(row=index + 2, column=int(col) + 1)
            cell.fill = highlight
        except ValueError:
            print(f"Skipping invalid index: row={index}, col={col}")

# Save the workbook as a new file
wb.save("file3.xlsx")
