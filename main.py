from ProcessHanddler.data_analyzer import *
from ProcessHanddler.chart_generator import *
from ProcessHanddler.data_cleaning import *
from ProcessHanddler.file_reader import *
from ProcessHanddler.quality_checker import *
from ProcessHanddler.report_generator import *
from ProcessHanddler.QwenModel_Client import QwenClient
from util.extract_file_KB import *
from util.PackData import *
from Idea_core.Pre_process_for_Model import *
def process(file_path):
    # 读取 Excel 文件
    data, data_id = read_excel(file_path)
    has_content, file_id_dir = create_and_check_directory(data_id)

    # 数据质量监测
    quality_report = check_quality(data)

    #数据清洗（此处涉及值传递，后续可能改为class类传递 方便管理中间值状态）
    clean_data = data_cleaning_general(data)

    # 初始化通义千问客户端
    qwen_client = QwenClient()

    # 数据分析
    analysis_results = analyze_data(clean_data,qwen_client)



    # 生成报告
    report = generate_report_general(quality_report,analysis_results)
    report_structured = generate_report_Json_structured(quality_report,analysis_results)
    # 生成图表
    selected_keys = ["histogram_img_base64", "scatter_img_base64"]
    chart_set = generate_chart_general(clean_data,analysis_results,file_id_dir)
    chart_base64 = {key: chart_set[key] for key in selected_keys if key in chart_set}
    #Img_path
    selected_keys = ["histogram_img_path", "scatter_img_path"]
    Img_path =  {key: chart_set[key] for key in selected_keys if key in chart_set}



    return {"report": report, "chart_base64": chart_base64}, Img_path,report_structured


def main():
    #file_path = 'test.xlsx' ## FE EXCEL API
    file_path = r'C:\Users\Administrator\Desktop\Project\C2Ev2\NeuroViz\test.xlsx'

    # 处理数据
    result,img_path,report_structured = process(file_path) ## process API
    
    # Idea from Qwen
    Idea_All = get_response_Idea(img_path,result['report'])

    #print(result['report'])
    #print(f"Chart Base64: {result['chart_base64']}")
    #print(Idea_All)
    
    # Pack all the data to FE Json format
    json_report = PackDataToJson(report_structured,img_path,result['chart_base64'],Idea_All)
    print(json_report)

    
if __name__ == "__main__":
    main()