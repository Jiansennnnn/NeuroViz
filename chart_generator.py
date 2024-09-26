import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import os
import seaborn as sns


def generate_chart_general(data,analysis_results):
    try:
        # 生成直方图
        histogram_img_base64 = generate_graph_histogram(data)

        # 生成散点图
        scatter_img_base64 = generate_scatter_plot(data,analysis_results)

        return {
            "histogram_img_base64": histogram_img_base64,
            "scatter_img_base64": scatter_img_base64
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


def generate_graph_histogram(data):
    # 图片存储地址
    output_path = 'graph_place/graph_histogram'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 生成直方图
    plt.figure(figsize=(10, 6))
    numeric_columns = data.select_dtypes(include='number').columns
    data[numeric_columns].hist(bins=20, color='blue', edgecolor='black', linewidth=1.0)
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'chart_histogram_{timestamp}.png'

    # 保存图表到文件
    file_path = output_path + "/" + filename
    plt.savefig(file_path)
    plt.close()
    return img_base64


def generate_scatter_plot(data, analysis_results):
    # 图片存储地址
    output_path = 'graph_place/graph_scatter'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    numeric_columns = data.select_dtypes(include='number').columns

    x = analysis_results['xy_fields']['x']
    y = analysis_results['xy_fields']['y']

    if x and y:
        x_column = x
        y_column = y
    else:
        # 默认选择前两个数值列作为X轴和Y轴
        x_column = numeric_columns[1]
        y_column = numeric_columns[0]

    # 生成散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column], color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Scatter Plot of {x_column} vs {y_column}')

    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'scatter_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    plt.close()

    return img_base64


def generate_chart_customized(data):
    pass
