import pandas as pd
import random
import re
def generate_random_id(length=8):
    return random.randint(10**(length-1), (10**length)-1)


def clean_header(header):
    """remove special characters in all headers"""
    return re.sub(r'[^\w\s]', '', header).strip()



# 读取 Excel 文件
def read_excel(file_path):
    random_id = generate_random_id()
    
    #clearn headers
    df = pd.read_excel(file_path, engine='openpyxl')
    new_headers = [clean_header(header) for header in df.columns]
    df.columns = new_headers
    return df, random_id















### TO DO LIST 
#CSV (Comma-Separated Values)
#TXT (Text)
#JSON 
#XML 
#SQL 
#Access 
#PDF 
#SAS7BDAT / XPT