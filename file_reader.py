import pandas as pd
import random
def generate_random_id(length=8):
    return random.randint(10**(length-1), (10**length)-1)

# 读取 Excel 文件
def read_excel(file_path):
    random_id = generate_random_id()
    return pd.read_excel(file_path, engine='openpyxl'), random_id
