from flask import Flask, request, jsonify, flash, redirect, url_for
from ProcessHanddler.chart_generator import *
from ProcessHanddler.data_cleaning import *
from ProcessHanddler.file_reader import *
from ProcessHanddler.data_analyzer import *
from ProcessHanddler.quality_checker import *
from ProcessHanddler.report_generator import *
from ProcessHanddler.QwenModel_Client import *
from util.extract_file_KB import *
from util.PackData import *
from Idea_core.Pre_process_for_Model import *
import os
from flask_util.config import ALLOWED_EXTENSIONS,UPLOAD_LANDING_FOLDER, SCRIPT_PATH
from werkzeug.utils import secure_filename
import subprocess


logging.basicConfig(filename="backend_main.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


app = Flask(__name__)
logger.info(f"Flask instant: {app}")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def hello_world():
    return "<p>test!</p>"

@app.route('/FileHanddler', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"status": "error", "message": "File not in request.files"}), 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return jsonify({"status": "error", "message": "Filename empty"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) ## NEVER TRUST USER INPUT
            file.save(os.path.join(UPLOAD_LANDING_FOLDER, filename))
            return jsonify({"status": "succeed", "message": "Filename uploaded"}), 200
    return 


## Process logic entry
@app.route('/upload_and_process', methods=['GET'])
async def upload_and_process():
    filename = request.args.get('filename')
    if filename == '':
        return jsonify({"status": "error", "message": "Filename empty"}), 400
    else:
        try:
            file_location = os.path.join(UPLOAD_LANDING_FOLDER, filename)


            #! main process
            data, data_id = read_excel(file_location)
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
            
            
            #File backup
            backupfile(data_id)
            
            result,img_path,report_structured = {"report": report, "chart_base64": chart_base64}, Img_path, report_structured
            # Idea from Qwen
            Idea_All = get_response_Idea(img_path,result['report'])
            
            # Pack all the data to FE Json format
            json_report = PackDataToJson(report_structured,img_path,result['chart_base64'],Idea_All)
            json_source = PackSourceToJson(clean_data)
            
            return jsonify({
                "status": "succeed",
                "message": "Process Finished",
                "json_report": json_report,
                "json_source": json_source
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Error in generating response: {e}"}), 400

@app.route('/ClearHistoryFiles', methods=['GET'])
def ClearHistoryFiles():
    try:
        # 调用 Python 脚本
        subprocess.run(['python', SCRIPT_PATH], check=True)
        return jsonify({'message': 'History files cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 配置文件
app.config.from_object('flask.config.Config')
app.config
 

if __name__ == '__main__':
    # 注册蓝图
    #app.register_blueprint(main_bp)
    app.run(host='0.0.0.0', port= 7777, debug=True)