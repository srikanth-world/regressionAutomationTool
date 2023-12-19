import pandas as pd

def compare_and_merge_excel(file1_path, file2_path, columns_to_compare, file3_path):
    # Read data from Excel files
    excel1 = pd.ExcelFile(file1_path)
    excel2 = pd.ExcelFile(file2_path)

    # Initialize an Excel writer for the output file
    with pd.ExcelWriter(file3_path, engine='openpyxl') as writer:
        # Manually set visibility for a dummy sheet
        writer.book.create_sheet('dummy_sheet')
        writer.book['dummy_sheet'].sheet_state = 'hidden'
        writer.book.remove(writer.book['dummy_sheet'])

        # Iterate over each sheet in both Excel files
        for sheet_name in excel1.sheet_names:
            # Read data from the current sheet in both files
            df1 = excel1.parse(sheet_name)
            df2 = excel2.parse(sheet_name)

            # Compare dataframes based on specified columns
            merged_data = pd.merge(df1, df2, on=columns_to_compare, how='outer', suffixes=('_file1', '_file2'), indicator=True)

            # Identify added, updated, and deleted rows
            added_rows = merged_data.loc[lambda x: x['_merge'] == 'right_only']
            updated_rows = merged_data.loc[lambda x: x['_merge'] == 'both']
            deleted_rows = merged_data.loc[lambda x: x['_merge'] == 'left_only']

            # Highlight differences in the data
            differences_styled = pd.DataFrame(index=merged_data.index)
            differences_styled.loc[added_rows.index, :] = 'background: lightgreen'
            differences_styled.loc[updated_rows.index, :] = 'background: lightyellow'

            # Merge data from both files into a new dataframe
            merged_data = pd.merge(df1, df2, on=columns_to_compare, how='outer', suffixes=('_file1', '_file2'))

            # Write the differences and merged data to the output file with individual sheets
            differences_styled.to_excel(writer, sheet_name=f'Differences_{sheet_name}', index=False, header=False, engine='openpyxl', startrow=1)
            merged_data.to_excel(writer, sheet_name=f'MergedData_{sheet_name}', index=False)

# Example usage
file1_path = 'path/to/file1.xlsx'
file2_path = 'path/to/file2.xlsx'
columns_to_compare = ['Col1', 'Col2']  # Replace with the actual column names
file3_path = 'path/to/file3.xlsx'

compare_and_merge_excel(file1_path, file2_path, columns_to_compare, file3_path)
