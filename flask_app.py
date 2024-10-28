from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_cors import CORS
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
import socket



logging.basicConfig(filename="backend_main.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources=r'/*')
logger.info(f"Flask instant: {app}")

SESSION_TYPE="filesystem"
SECRETE_KEY = os.urandom(24)
logger.info(f"Flask secrete: {SECRETE_KEY}")

app.secret_key = SECRETE_KEY
app.config['SECRETE_KEY'] = SECRETE_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def serialize_dict(data):
    if isinstance(data, dict):
        return {k: serialize_dict(v) for k, v in data.items()}
    elif isinstance(data, pd.Series) or isinstance(data, pd.Index) or isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data

def find_file_by_uid(file_uid, upload_folder):

    for filename in os.listdir(upload_folder):
        # check if start with file_uid 
        if filename.startswith(file_uid):
            # filePath Construct
            file_location = os.path.join(upload_folder, filename)
            return file_location
    # exception
    return None


@app.route("/")
def hello_world():
    logger.info(f"Flask instant Entry gooooooooooooood: {app}")

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
        
        # check if file_uid exists
        file_uid = request.form.get('file_uid')
        logger.info(f"file_uid= {file_uid}")
        if not file_uid:
            return jsonify({"status": "error", "message": "File UID not provided"}), 400

        
        if file.filename == '':
            flash('No selected file')
            return jsonify({"status": "error", "message": "Filename empty"}), 400
        
        if file and allowed_file(file.filename):
            logger.info(f"file.filename= {file.filename}")
            filename = secure_filename(file.filename) ## NEVER TRUST USER INPUT
            filename = file_uid + "_" + filename
            file.save(os.path.join(UPLOAD_LANDING_FOLDER, filename))
            return jsonify({"status": "succeed", "message": "Filename uploaded"}), 200
    return jsonify({"status": "error", "message": "Invalid request method"}), 405


## Process logic entry
@app.route('/upload_and_process', methods=['GET'])
async def upload_and_process():
    file_uid = request.args.get('file_uid')
    if file_uid == '':
        return jsonify({"status": "error", "message": "file_uid empty"}), 400
    else:
        try:
            #file_location = os.path.join(UPLOAD_LANDING_FOLDER, filename)
            file_location = find_file_by_uid(file_uid, UPLOAD_LANDING_FOLDER)
            if file_location:
                logger.info(f"matched file_location= {file_location}")
            else:
                logger.info(f"No matched file_location= {file_location}")
                return jsonify({"status": "error", "message": "No matched file_location"}), 405
            
            
            logger.info("............Starting main process.........")
            #! main process
            data, data_id = read_excel(file_location)
            logger.info("**read_excel**............ succeeded")
            has_content, file_id_dir = create_and_check_directory(data_id)

            # 数据质量监测
            quality_report = check_quality(data)
            logger.info("**quality_report**............ succeeded")
            #数据清洗（此处涉及值传递，后续可能改为class类传递 方便管理中间值状态）
            clean_data = handle_missing_and_outliers(data)
            logger.info("**clean_data**............ succeeded")

            # 初始化通义千问客户端
            qwen_client = QwenClient()

            # 数据分析
            logger.info(data)
            logger.info(clean_data)
            analysis_results,start_count = analyze_data(clean_data,qwen_client) #! CAll 1
            logger.info(clean_data)
            logger.info("**analyze_data**............ succeeded")
            
            # asyncio to get comment for Corr picture
            #executor = ThreadPoolExecutor()
            #corr_comment = executor.submit(partial(run_comp_stat, analysis_results['correlation_matrix'], analysis_results['xy_fields'], analysis_results['statistical_fields'] ))
            #! Call 2
            corr_field_info = analysis_results['xy_fields']['x'].split(', ') + [analysis_results['xy_fields']['y']]
            corr_comment = await Get_comment(analysis_results['correlation_matrix'], corr_field_info, analysis_results['descriptive_statistics'])
            
            # 生成报告
            report = generate_report_general(quality_report,analysis_results)
            report_structured = generate_report_Json_structured(quality_report,analysis_results)
            logger.info("**generate_report_general**............ succeeded")

            # 生成图表
            selected_keys = ["histogram_img_base64", "scatter_img_base64"]
            chart_set = generate_chart_general(clean_data,analysis_results,file_id_dir)
            logger.info("**generate_chart_general**............ succeeded")

            chart_base64 = {key: chart_set[key] for key in selected_keys if key in chart_set}
            #Img_path
            selected_keys = ["histogram_img_path", "scatter_img_path"]
            Img_path =  {key: chart_set[key] for key in selected_keys if key in chart_set}
            #Img_range
            selected_keys = ["histogram_img_range", "scatter_img_range","line_img_range", "pie_img_range", "Kmean_img_range"]
            Img_range =  {key: chart_set[key] for key in selected_keys if key in chart_set}
            Img_range_serializable = serialize_dict(Img_range)
            
                
            #File backup
            backupfile(data_id)
            logger.info("**backupfile**............ succeeded")

            result,img_path,report_structured = {"report": report, "chart_base64": chart_base64}, Img_path, report_structured
            # Idea from Qwen
            Idea_All = get_response_Idea(img_path,result['report']) #! Call 3
            logger.info("**Idea_Core_logics**............ succeeded")
            
            # Pack all the data to FE Json format
            json_report = PackDataToJson(report_structured,img_path,result['chart_base64'],Idea_All)
            json_source = PackSourceToJson(clean_data)
            logger.info("**Pack all the data to FE Json format**............ succeeded")
            
            
            return jsonify({
                "status": "succeed",
                "message": "Process Finished",
                "json_report": json_report,
                "json_source": json_source,
                "start_count" : start_count,
                "corr_comment": corr_comment,
                "Img_range" : Img_range_serializable

            }), 200
        except Exception as e:
            logger.info(f"Process Logic Failed in = {e}")
            return jsonify({"status": "error", "message": f"Error in generating response: {e}"}), 400

@app.route('/ClearHistoryFiles', methods=['GET'])
def ClearHistoryFiles():
    try:
        
        subprocess.run(['python', SCRIPT_PATH], check=True)
        return jsonify({'message': 'History files cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # 注册蓝图
    #app.register_blueprint(main_bp)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    port = 7777
    print(f"App is running at http://{ip_address}:{port}")
    app.run(host='0.0.0.0', port= 7777, debug=False)
