import pandas as pd
from openpyxl.styles import PatternFill
from openpyxl import load_workbook

def compare_and_highlight_changes(old_df, new_df, sheet_name, output_path):
    # Merge dataframes on a common key (assuming there is a unique identifier)
    merged_df = pd.merge(old_df, new_df, on='common_key', how='outer', suffixes=('_old', '_new'))

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

    # Write the merged data to a new Excel sheet.
    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets[sheet_name]

    # Get the dimensions of the DataFrame.
    num_rows, num_cols = merged_df.shape

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

    # Iterate through all the columns.
    for col_num, value in enumerate(merged_df.columns.values):
        # Define the default cell format with no fill.
        cell_format = workbook.add_format({'bg_color': '#FFFFFF'})

        # Check if the column header is in the old or new dataframe.
        if '_old' in value:
            cell_format.set_bg_color('#FFC7CE')  # Light red fill for old values.
        elif '_new' in value:
            cell_format.set_bg_color('#C6EFCE')  # Light green fill for new values.

        # Set the column header cell format.
        worksheet.write(0, col_num, value, cell_format)

        # Set the column width and format.
        worksheet.set_column(col_num, col_num, len(value) + 2)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

# Example usage
old_excel_path = 'path/to/old_excel.xlsx'
new_excel_path = 'path/to/new_excel.xlsx'
output_excel_path = 'path/to/output_excel.xlsx'

old_sheets = pd.read_excel(old_excel_path, sheet_name=None)
new_sheets = pd.read_excel(new_excel_path, sheet_name=None)

for sheet_name in old_sheets.keys():
    old_df = old_sheets[sheet_name]
    new_df = new_sheets[sheet_name]

    compare_and_highlight_changes(old_df, new_df, sheet_name, output_excel_path)
