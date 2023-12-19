import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def compare_and_merge(file1_path, file2_path, columns_to_compare, output_file_path):
    # Read Excel files into Pandas dataframes
    df1 = pd.read_excel(file1_path, sheet_name=None)
    df2 = pd.read_excel(file2_path, sheet_name=None)

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        # Iterate through all sheets in both files
        for sheet_name in set(df1.keys()) | set(df2.keys()):
            # Get the dataframes for the current sheet (or empty dataframe if sheet not present)
            sheet_df1 = df1.get(sheet_name, pd.DataFrame())
            sheet_df2 = df2.get(sheet_name, pd.DataFrame())

            # Merge dataframes on specified columns
            merged_df = pd.merge(sheet_df1, sheet_df2, how='outer', on=columns_to_compare, indicator=True)

            # Create a Pandas Excel writer for the current sheet
            merged_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)

            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Ensure the sheet is visible
            workbook[sheet_name].sheet_state = 'visible'

            # Get the xlsxwriter writer objects
            xlsxwriter_writer = pd.ExcelWriter(output_file_path, engine='openpyxl')
            xlsxwriter_workbook = xlsxwriter_writer.book
            xlsxwriter_worksheet = xlsxwriter_writer.sheets[sheet_name]

            # Define cell formats and highlight differences
            fill = PatternFill(start_color="yellow", end_color="yellow", fill_type="solid")
            for row in range(1, len(merged_df) + 2):
                if worksheet.cell(row=row, column=len(merged_df.columns) + 3).value == 'both':
                    for col in range(1, len(merged_df.columns) + 1):
                        xlsxwriter_worksheet.cell(row=row, column=col).fill = fill

            # Close the Pandas Excel writer for the current sheet
            xlsxwriter_writer.save()

# Example usage
compare_and_merge('file1.xlsx', 'file2.xlsx', ['Column1', 'Column2'], 'file3.xlsx')
