!pip install --upgrade -q gspread

from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default

# sheet_name: the name of the Google Spreadsheet with the data you want to input in the form of (row_len)x(col_len)
# After this function is executed, you'll get the data in the form of a one-dimentional list.
def data_input(sheet_name, row_len, col_len):
    creds, _ = default()

    gc = gspread.authorize(creds)

    sht = gc.open(sheet_name)
    worksheet = sht.get_worksheet(0)

    cells = worksheet.range(1, 1, row_len, col_len)

    table_data = []

    for i, cell in enumerate(cells):
        if cell.value == "":
            continue
        table_data.append(float(cell.value))

    return table_data

# sheet_name: the name of the Google Spreadsheet with the data you want to output in the form of (len(data))x(len(data[0]))
def file_output(data, sheet_name):
    creds, _ = default()

    gc = gspread.authorize(creds)

    row_len = len(data)
    col_len = len(data[0])

    sh = gc.create(sheet_name)
    worksheet = gc.open(sheet_name).sheet1

    worksheet.add_rows(row_len)

    cell_list = worksheet.range(1, 1, row_len, col_len)
    col_list = [flatten for inner in data for flatten in inner]

    for cell, col in zip(cell_list, col_list):
      cell.value = col

    worksheet.update_cells(cell_list)
