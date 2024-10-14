import pandas as pd
import random, os, shutil
import re
from flask_util.config import UPLOAD_LANDING_FOLDER, ALLOWED_EXTENSIONS
def generate_random_id(length=8):
    return random.randint(10**(length-1), (10**length)-1)


def clean_header(header):
    """remove special characters in all headers"""
    return re.sub(r'[^\w\s]', '', header).strip()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 读取 Excel 文件
def read_excel(file_path):
    random_id = generate_random_id()
    
    #clearn headers
    df = pd.read_excel(file_path, engine='openpyxl')
    new_headers = [clean_header(header) for header in df.columns]
    df.columns = new_headers
    return df, random_id


#backup file to IDbased folder
def backupfile(id_name):
    OUTPUT_PATH = 'flask_util/backup'
    if not os.path.exists(UPLOAD_LANDING_FOLDER):
        print("Fatal Error: Upload folder does not exist.")
        return
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        
    output_folder = os.path.join(OUTPUT_PATH, str(id_name))
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    for file_name in os.listdir(UPLOAD_LANDING_FOLDER):
        if allowed_file(file_name):
            # source file path
            source_file = os.path.join(UPLOAD_LANDING_FOLDER, file_name)
            # target file path
            destination_file = os.path.join(output_folder, file_name)
            # copy file to destination folder
            shutil.copy(source_file, destination_file)
            print(f"Copied {file_name} to {output_folder}")
            
            os.remove(source_file)

            print(f"Deleted {file_name} from Landing Place : {UPLOAD_LANDING_FOLDER}")
  
    













### TO DO LIST 
#CSV (Comma-Separated Values)
#TXT (Text)
#JSON 
#XML 
#SQL 
#Access 
#PDF 
#SAS7BDAT / XPT