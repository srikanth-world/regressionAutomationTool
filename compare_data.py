from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def compare_and_merge(file1_path, file2_path, columns_to_compare, output_file_path):
    # Load Excel files using openpyxl
    workbook1 = load_workbook(file1_path)
    workbook2 = load_workbook(file2_path)

    # Create a new workbook for the output
    output_workbook = load_workbook(output_file_path)

    # Iterate through sheets in both files
    for sheet_name in set(workbook1.sheetnames) | set(workbook2.sheetnames):
        # Get worksheets for the current sheet (or create a new one if sheet not present)
        worksheet1 = workbook1[sheet_name] if sheet_name in workbook1.sheetnames else workbook1.create_sheet(title=sheet_name)
        worksheet2 = workbook2[sheet_name] if sheet_name in workbook2.sheetnames else workbook2.create_sheet(title=sheet_name)
        output_worksheet = output_workbook[sheet_name] if sheet_name in output_workbook.sheetnames else output_workbook.create_sheet(title=sheet_name)

        # Create a new worksheet for the output
        output_worksheet = output_workbook.create_sheet(title=sheet_name)

        # Copy the headers to the output worksheet
        for col_num, value in enumerate(worksheet1.iter_cols(values_only=True, max_row=1), start=1):
            output_worksheet.cell(row=1, column=col_num, value=value[0])

        # Merge data from both worksheets on specified columns
        for row_num, (row1, row2) in enumerate(zip(worksheet1.iter_rows(min_row=2, values_only=True),
                                                  worksheet2.iter_rows(min_row=2, values_only=True)), start=2):
            output_worksheet.append(row1 + row2)

            # Highlight differences in the specified columns
            for col_num, (cell1, cell2) in enumerate(zip(row1, row2), start=1):
                if col_num in columns_to_compare and cell1 != cell2:
                    output_worksheet.cell(row=row_num, column=col_num).fill = PatternFill(start_color="yellow", end_color="yellow", fill_type="solid")

    # Save the output workbook
    output_workbook.save(output_file_path)

# Example usage
compare_and_merge('file1.xlsx', 'file2.xlsx', [1, 2], 'file3.xlsx')
