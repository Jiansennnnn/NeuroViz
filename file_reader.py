import pandas as pd


# 读取 Excel 文件
def read_excel(file_path):
    return pd.read_excel(file_path, engine='openpyxl')
