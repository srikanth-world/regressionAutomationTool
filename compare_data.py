import os
import pandas as pd
from openpyxl import load_workbook
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

        # Create a new workbook
        merged_workbook = Workbook()

        # Load Excel files into pandas dataframes
        df1 = pd.read_excel(file1_path, engine='openpyxl', sheet_name=None)
        df2 = pd.read_excel(file2_path, engine='openpyxl', sheet_name=None)

        # Create a writer for the merged and highlighted dataframe
        writer = pd.ExcelWriter(os.path.join(output_path, f'Merged_{file}'), engine='openpyxl')
        writer.book = load_workbook(os.path.join(output_path, f'Merged_{file}'))

        # Iterate through sheets
        for sheet_name in set(df1.keys()).intersection(df2.keys()):
            # Get dataframes for each sheet
            sheet_df1 = df1[sheet_name]
            sheet_df2 = df2[sheet_name]

            # Compare dataframes cell by cell
            diff = (sheet_df1 != sheet_df2)

            # Highlight differences in the merged dataframe
            diff_styled = pd.DataFrame(index=sheet_df1.index, columns=sheet_df1.columns)
            diff_styled = diff_styled.style.applymap(lambda x: 'background-color: yellow', subset=pd.IndexSlice[diff])

            # Write the merged and highlighted dataframe to the Excel file
            diff_styled.to_excel(writer, index=False, sheet_name=sheet_name)

        # Save the merged and highlighted workbook
        writer.save()

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
