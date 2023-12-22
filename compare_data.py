import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

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

            # Ensure both DataFrames have the same indices and columns
            common_index = sheet_df1.index.union(sheet_df2.index)
            common_columns = sheet_df1.columns.union(sheet_df2.columns)

            sheet_df1 = sheet_df1.reindex(index=common_index, columns=common_columns, fill_value=None)
            sheet_df2 = sheet_df2.reindex(index=common_index, columns=common_columns, fill_value=None)

            # Identify differences
            diff_cells = (sheet_df1.values != sheet_df2.values)

            # Merge old and new data
            merged_df = sheet_df1.combine_first(sheet_df2)

            # Create a Pandas Styler object to highlight differences in yellow
            styler = merged_df.style.applymap(lambda x: 'background-color: yellow' if diff_cells.at[x] else '', subset=diff_cells)

            # Create a new sheet in the merged workbook
            merged_sheet = merged_workbook.create_sheet(title=sheet_name)

            # Write the header row
            header_row = list(merged_df.columns)
            merged_sheet.append(header_row)

            # Write data to the sheet using dataframe_to_rows
            for row in dataframe_to_rows(merged_df, index=False, header=False):
                merged_sheet.append(row)

            # Apply the styling
            for row in merged_sheet.iter_rows(min_row=2, max_row=merged_sheet.max_row, min_col=1, max_col=merged_sheet.max_column):
                for cell in row:
                    cell.style = styler.use_diff_style(diff_cells, cell.coordinate)

        # Remove the default sheet created by openpyxl
        merged_workbook.remove(merged_workbook.active)

        # Save the merged workbook
        merged_workbook.save(os.path.join(output_path, f'Merged_{file}'))

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
