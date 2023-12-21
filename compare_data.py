import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def compare_and_merge(path1, path2, output_path):
    # Get all Excel files in the given paths
    files1 = [f for f in os.listdir(path1) if f.endswith('.xlsx')]
    files2 = [f for f in os.listdir(path2) if f.endswith('.xlsx')]

    # Iterate through common files
    for file in set(files1).intersection(files2):
        file1_path = os.path.join(path1, file)
        file2_path = os.path.join(path2, file)

        # Load Excel files into pandas dataframes
        df1 = pd.read_excel(file1_path, engine='openpyxl', sheet_name=None, header=1)
        df2 = pd.read_excel(file2_path, engine='openpyxl', sheet_name=None, header=1)

        # Create a new workbook
        merged_workbook = Workbook()

        # Iterate through sheets
        for sheet_name in set(df1.keys()).union(df2.keys()):
            # Get dataframes for each sheet
            sheet_df1 = df1.get(sheet_name, pd.DataFrame())
            sheet_df2 = df2.get(sheet_name, pd.DataFrame())

            # Identify differences
            diff_cells = (sheet_df1 != sheet_df2)

            # Merge old and new data
            merged_df = sheet_df1.combine_first(sheet_df2)

            # Create a Pandas Styler object to highlight differences in yellow
            styler = merged_df.style.applymap(lambda x: 'background-color: yellow' if diff_cells.at[x] else '', subset=diff_cells)

            # Get the active sheet from the new workbook
            sheet = merged_workbook.active
            # Convert the styled DataFrame to Excel
            pd.io.formats.excel.format.ExcelFormatter(styler).write(sheet)

        # Save the merged and highlighted workbook
        merged_workbook.save(os.path.join(output_path, f'Merged_{file}'))

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
