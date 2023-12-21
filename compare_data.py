import os
import pandas as pd
from openpyxl import load_workbook
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
        df1 = pd.read_excel(file1_path, engine='openpyxl', sheet_name=None)
        df2 = pd.read_excel(file2_path, engine='openpyxl', sheet_name=None)

        # Find differences between dataframes
        diff = pd.concat([df1[key] for key in df1] + [df2[key] for key in df2]).drop_duplicates(keep=False)

        # Highlight differences in the merged dataframe
        diff_styled = diff.style.applymap(lambda x: 'background-color: yellow', subset=pd.IndexSlice[:, :])

        # Write the merged and highlighted dataframe to a new Excel file
        with pd.ExcelWriter(os.path.join(output_path, f'Merged_{file}'), engine='openpyxl') as writer:
            for sheet_name, sheet_df in diff.items():
                sheet_df.to_excel(writer, index=False, sheet_name=sheet_name)
                writer.sheets[sheet_name].sheet_view.tabSelected = True

if __name__ == "__main__":
    # Replace these paths with your actual paths
    path1 = 'path/to/excels1'
    path2 = 'path/to/excels2'
    output_path = 'path/to/output'

    compare_and_merge(path1, path2, output_path)
