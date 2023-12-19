import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Function to read data from a worksheet and return a DataFrame
def read_data(sheet, start_row):
    data = []
    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        data.append(row)
    return pd.DataFrame(data, columns=data[0])

# Function to compare two DataFrames and highlight the differences in the Excel file
def highlight_differences(df1, df2, sheet, fill_color="FFFF00"):
    for col in df1.columns:
        for row in df1.index:
            if df1.at[row, col] != df2.at[row, col]:
                cell = sheet.cell(row=row + df1_start_row, column=df1.columns.get_loc(col) + 1)
                cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

# Load the workbook and select the first sheet
file_path = 'path/to/your/file.xlsx'  # Update with the actual file path
wb = load_workbook(file_path)
sheet = wb.active

# Find the positions of Q02 and Q03 in the sheet
q02_position = None
q03_position = None

for row in sheet.iter_rows(values_only=True):
    if "Q02" in row:
        q02_position = row
    elif "Q03" in row:
        q03_position = row

# Read data into DataFrames
if q02_position and q03_position:
    # Find the positions to split the data
    q02_start_row = sheet.cell(row=sheet.min_row, column=sheet.max_column).row + 2
    q03_start_row = sheet.cell(row=sheet.min_row, column=sheet.max_column).row + 1

    # Read Q02 data
    df_q02 = read_data(sheet, q02_start_row)

    # Read Q03 data
    df_q03 = read_data(sheet, q03_start_row)

    # Highlight differences
    highlight_differences(df_q02, df_q03, sheet)

    # Save the workbook
    wb.save('path/to/your/output_file.xlsx')  # Update with the desired output file path
else:
    print("Q02 or Q03 not found in the sheet.")
