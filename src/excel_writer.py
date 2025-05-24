import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def write_to_excel(rows, output_file="output.xlsx", sheet_name="April 2025"):
    df = pd.DataFrame(rows, columns=["Date", "Description", "Category", "Rephrased", "Amount"])

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    wb.save(output_file)