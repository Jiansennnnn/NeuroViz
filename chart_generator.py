import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import base64
from datetime import datetime
import os
import seaborn as sns


def generate_chart_general(data,analysis_results,id_path):
    plt.ioff()
    try:
        # 生成直方图
        histogram_img_base64, histogram_img_path = generate_graph_histogram(data,id_path,analysis_results['xy_fields'])

        # 生成散点图
        scatter_img_base64, scatter_img_path = generate_scatter_plot(data,analysis_results,id_path)

        return {
            "histogram_img_base64": histogram_img_base64,
            "scatter_img_base64": scatter_img_base64,
            "histogram_img_path": histogram_img_path,
            "scatter_img_path" : scatter_img_path 
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


def generate_graph_histogram(data,id_path,xyfields):
    # 图片存储地址
    output_path = 'graph_place/graph_histogram'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    '''
    # 生成直方图
    plt.figure(figsize=(10, 6))
    numeric_columns = data.select_dtypes(include='number').columns
    data[numeric_columns].hist(bins=20, color='blue', edgecolor='black', linewidth=1.0)
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    '''
    
    
    # unpacked xyfields
    x_fields = xyfields['x'].split(', ')
    y_field = xyfields['y']
    
    #validate fields
    valid_x_fields = [field for field in x_fields if field in data.columns]
    if not valid_x_fields or y_field not in data.columns:
        raise ValueError("Invalid fields provided.")
    
    #color mapping
    cmap = cm.get_cmap('tab20', len(valid_x_fields))
    colors = [cmap(i) for i in range(len(valid_x_fields))]
    
    # historgram for multi independent variables
    num_plots = len(valid_x_fields)
    fig, axs = plt.subplots(nrows=1, ncols=num_plots, figsize=(10 * num_plots, 6))
    
    
    # Histogram for each X field
    for i, field in enumerate(valid_x_fields):
        ax = axs if num_plots == 1 else axs[i]
        if field in data.columns and not data[field].isnull().all():

            ax.hist(data[field], bins=20, alpha=0.5, label=field, density=True, color=colors[i])
            ax.set_title(f'Distribution of {field}')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()

    plt.tight_layout()
    
    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'chart_histogram_{timestamp}.png'

    # 保存图表到文件
    file_path = output_path + "/" + filename
    plt.savefig(file_path)

    #save to file knowledgebaes by id
    file_path = os.path.join(id_path, filename)
    plt.savefig(file_path)
    
    #Base64 output
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_stream = buf.getvalue()
    img_base64 = base64.b64encode(img_stream).decode('utf-8')
    buf.close()    
    plt.close()
    return img_base64 ,file_path


def generate_scatter_plot(data, analysis_results,id_path):
    # 图片存储地址
    output_path = 'graph_place/graph_scatter'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    #numeric_columns = data.select_dtypes(include='number').columns

    # unpacked xyfields
    x_fields = analysis_results['xy_fields']['x'].split(', ')
    y_field = analysis_results['xy_fields']['y']
    
    #validate fields
    valid_x_fields = [field for field in x_fields if field in data.columns]
    if not valid_x_fields or y_field not in data.columns:
        raise ValueError("Invalid fields provided.")
    
    #color mapping
    cmap = cm.get_cmap('tab20', len(x_fields))  
    colors = [cmap(i) for i in range(len(x_fields))]
    
    # Scatter plots for each X field
    num_plots = len(valid_x_fields)
    fig, axs = plt.subplots(nrows=1, ncols=num_plots, figsize=(10 * num_plots, 6))

    for i, x_field in enumerate(valid_x_fields):
        ax = axs if num_plots == 1 else axs[i]
        if x_field in data.columns and y_field in data.columns:
            ax.scatter(data[x_field], data[y_field], color=colors[i], edgecolor='black', alpha=0.7, label=x_field)
            ax.set_title(f'Scatter Plot of {x_field} vs {y_field}')
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            ax.legend()

    plt.tight_layout()
    '''
    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    '''
    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    filename = f'scatter_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    
    #save to file knowledgebaes by id
    file_path = os.path.join(id_path, filename)
    plt.savefig(file_path)
    plt.close()

    #Base64 output
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_stream = buf.getvalue()
    img_base64 = base64.b64encode(img_stream).decode('utf-8')
    buf.close()    
    plt.close()
    return img_base64 ,file_path


def generate_chart_customized(data):
    pass
