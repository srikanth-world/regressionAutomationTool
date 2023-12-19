import os
import pandas as pd

def compare_and_merge(folder1, folder2, output_folder):
    # Step 1: Get a list of all Excel files in folder1 and folder2
    excel_files_folder1 = [f for f in os.listdir(folder1) if f.endswith('.xlsx')]
    excel_files_folder2 = [f for f in os.listdir(folder2) if f.endswith('.xlsx')]

    # Step 2: Compare and merge Excel files
    for file1 in excel_files_folder1:
        if file1 in excel_files_folder2:
            print(f"Processing file: {file1}")

            try:
                # Load Excel files into DataFrames
                df1 = pd.read_excel(os.path.join(folder1, file1))
                df2 = pd.read_excel(os.path.join(folder2, file1))
                
                # Align DataFrames based on columns and indexes
                df1, df2 = df1.align(df2, axis=1, join='outer')
                df1, df2 = df1.align(df2, axis=0, join='outer')

            except Exception as e:
                print(f"Error reading files {file1}: {e}")
                continue

            # Compare and highlight differences
            df_diff = df1.compare(df2)

            # Step 3: Save the merged DataFrame to a new Excel file in the output folder
            output_file_path = os.path.join(output_folder, f'merged_{file1}')
            df_diff.to_excel(output_file_path, sheet_name='Differences', index=False)

            print(f"File saved to: {output_file_path}")

if __name__ == "__main__":
    folder1 = r'C:\data\old\folder1'
    folder2 = r'C:\data\old\folder2'
    output_folder = r'C:\data\old\folder3'

    compare_and_merge(folder1, folder2, output_folder)
