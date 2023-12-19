import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Function to highlight differences in Excel sheet
def highlight_differences(df1, df2, sheet, fill_color="FFFF00"):
    for col in df1.columns:
        for row in df1.index:
            if df1.at[row, col] != df2.at[row, col]:
                cell = sheet.cell(row=row + 2, column=df1.columns.get_loc(col) + 1)
                cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

# Reading two Excel sheets
sheet1 = pd.read_excel(r'Book1.xlsx')
sheet2 = pd.read_excel(r'Book2.xlsx')

# Compare two dataframes
differences = (sheet1 != sheet2).stack()

# Create a dataframe of differences
changed = differences[differences].reset_index()
changed.columns = ["Row", "Column", "Sheet1", "Sheet2"]

# Write the full data to output Excel file
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    sheet1.to_excel(writer, sheet_name='Sheet1', index=False)
    sheet2.to_excel(writer, sheet_name='Sheet2', index=False)

    # Access the output Excel file
    workbook = writer.book
    sheet = workbook['Sheet1']

    # Highlight the differences in Sheet1
    highlight_differences(sheet1, sheet2, sheet)

    # Save the workbook
    writer.save()
