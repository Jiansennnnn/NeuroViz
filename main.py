from file_reader import *
from quality_checker import *
from data_analyzer import *
from report_generator import *
from chart_generator import *
from data_cleaning import *
from util.extract_file_KB import *
import logging
from Pre_process_for_Model import *
#TEST
#from 
logging.basicConfig(filename="main.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def process(file_path):
    # 读取 Excel 文件
    data, data_id = read_excel(file_path)
    has_content, file_id_dir = create_and_check_directory(data_id)
    
    # 数据质量监测
    quality_report = check_quality(data)

    #数据清洗（此处涉及值传递，后续可能改为class类传递 方便管理中间值状态）
    clean_data = data_cleaning_general(data)
    
    # 数据分析
    analysis_results,response_variable,correlations = analyze_data_general(clean_data)
    #print(response_variable, correlations) #Correlation matrix for general analysis

    # 生成报告
    report = generate_report_general(quality_report, analysis_results)

    # 生成图表
    selected_keys = ["histogram_img_base64", "scatter_img_base64"]
    chart_set = generate_chart_general(clean_data,file_id_dir)
    chart_base64 = {key: chart_set[key] for key in selected_keys if key in chart_set}
    #Img_path
    selected_keys = ["histogram_img_path", "scatter_img_path"]
    Img_path =  {key: chart_set[key] for key in selected_keys if key in chart_set}
    

    response = get_response_FactorDetermination(Img_path, report,correlations)
    print(response)
    return {"report": report, "chart_base64": chart_base64, "corr_matrix": correlations} 


def main():
    file_path = r'C:\Users\Jiansen\Desktop\Project\C2E-startUp\C2eStartUp\test.xlsx'

    # 处理数据
    result = process(file_path)
    
    print(result['report'])
    print(result['corr_matrix'])
    #print(f"Chart Base64: {result['chart_base64']}")
    

if __name__ == "__main__":
    main()