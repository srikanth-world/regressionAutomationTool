import os
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl.styles

def compare_and_merge(path1, path2, output_path):
    # Get all Excel files in the given paths
    files1 = [f for f in os.listdir(path1) if f.endswith('.xlsx')]
    files2 = [f for f in os.listdir(path2) if f.endswith('.xlsx')]

    # Iterate through common files
    for file in set(files1).intersection(files2):
        file1_path = os.path.join(path1, file)
        file2_path = os.path.join(path2, file)

        # Load Excel files into pandas dataframes
        df1 = pd.read_excel(file1_path, engine='openpyxl', sheet_name=None, header=None)
        df2 = pd.read_excel(file2_path, engine='openpyxl', sheet_name=None, header=None)

        # Create a new workbook
        merged_workbook = Workbook()

        # Iterate through sheets
        for sheet_name in set(df1.keys()).union(df2.keys()):
            # Get dataframes for each sheet
            sheet_df1 = df1.get(sheet_name, pd.DataFrame())
            sheet_df2 = df2.get(sheet_name, pd.DataFrame())

            # Skip if both dataframes are empty
            if sheet_df1.empty and sheet_df2.empty:
                continue

            # Create a new sheet in the merged workbook
            merged_sheet = merged_workbook.create_sheet(title=sheet_name)

            # Write data from the first dataset with header
            if not sheet_df1.empty:
                merged_sheet.append([f'\n{sheet_name} from File 1'])
                for row in dataframe_to_rows(sheet_df1, index=False, header=True):
                    merged_sheet.append(row)

            # Write an empty row as a separator
            merged_sheet.append([])

            # Write data from the second dataset with header
            if not sheet_df2.empty:
                merged_sheet.append([f'\n{sheet_name} from File 2'])
                for row in dataframe_to_rows(sheet_df2, index=False, header=True):
                    merged_sheet.append(row)

            # Identify unique values and highlight in the merged sheet
            highlight_unique_values(merged_sheet, sheet_df1, sheet_df2)

        # Save the merged workbook
        merged_workbook.save(os.path.join(output_path, f'Merged_{file}'))

def highlight_unique_values(merged_sheet, sheet_df1, sheet_df2):
    # Ensure that the diff_cells DataFrame has the same indices as the merged_df DataFrame
    sheet_df1 = sheet_df1.set_index(list(sheet_df1.columns))
    sheet_df2 = sheet_df2.set_index(list(sheet_df2.columns))
    merged_sheet = merged_sheet.set_index(list(merged_sheet.columns))

    # Identify unique values in each column
    unique_values = sheet_df1[~sheet_df1.index.isin(sheet_df2.index)]

    # Iterate through columns to highlight unique values
    for col_idx, col in enumerate(sheet_df1.columns, start=1):
        for row_idx, cell in enumerate(merged_sheet[col], start=2):
            if row_idx <= len(unique_values) and cell.value == unique_values.at[unique_values.index[row_idx - 1], col]:
                cell.fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
