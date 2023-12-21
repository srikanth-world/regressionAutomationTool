import os
import pandas as pd
from openpyxl import Workbook

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

        # Create an ExcelWriter object
        writer = pd.ExcelWriter(os.path.join(output_path, f'Merged_{file}'), engine='openpyxl')
        writer.book = merged_workbook

        # Iterate through sheets
        for sheet_name in set(df1.keys()).union(df2.keys()):
            # Get dataframes for each sheet
            sheet_df1 = df1.get(sheet_name, pd.DataFrame())
            sheet_df2 = df2.get(sheet_name, pd.DataFrame())

            # Merge old and new data, handling the index mismatch
            merged_df = sheet_df1.merge(sheet_df2, how='outer', left_index=True, right_index=True, suffixes=('_1', '_2'))

            # Identify differences
            diff_cells = (merged_df.filter(like='_1').values != merged_df.filter(like='_2').values)

            # Create a Pandas Styler object to highlight differences in yellow
            styler = merged_df.style.applymap(lambda x: 'background-color: yellow' if diff_cells.at[x] else '', subset=diff_cells)

            # Write the merged and highlighted dataframe to the Excel file
            styler.to_excel(writer, index=False, sheet_name=sheet_name)

        # Save the merged and highlighted workbook
        writer.save()

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
