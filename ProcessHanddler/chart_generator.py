import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import pandas as pd
import base64
from datetime import datetime
import os
import seaborn as sns
from sklearn.cluster import KMeans

def generate_chart_general(data,analysis_results,id_path):
    plt.ioff()
    try:
        # 生成直方图
        histogram_img_base64, histogram_img_path, histogram_img_range = generate_graph_histogram(data,id_path,analysis_results['xy_fields'])

        # 生成散点图
        scatter_img_base64, scatter_img_path, scatter_img_range = generate_scatter_plot(data,analysis_results,id_path)

        # 生成折线图
        line_img_base64, line_img_path, line_img_range = generate_line_chart(data, analysis_results,id_path)
        ## example : line_img_range['age']['y_range_point']
        
        # 生成饼图
        pie_img_base64, pie_img_path, pie_img_range = generate_pie_chart(data, analysis_results,id_path)
        
        # Kmean
        Kmean_img_base64, Kmean_img_path, Kmean_img_range = generate_line_Kbean_chart(data, analysis_results,id_path)

        return {
            "histogram_img_base64": histogram_img_base64,
            "scatter_img_base64": scatter_img_base64,
            "line_img_base64": line_img_base64,
            "pie_img_base64": pie_img_base64,
            "Kmean_img_base64": Kmean_img_base64,
            "histogram_img_path": histogram_img_path,
            "scatter_img_path" : scatter_img_path,
            "line_img_path": line_img_path,
            "pie_img_path": pie_img_path, 
            "Kmean_img_path": Kmean_img_path,
            "histogram_img_range": histogram_img_range,
            "scatter_img_range": scatter_img_range,
            "line_img_range": line_img_range,
            "pie_img_range": pie_img_range,
            "Kmean_img_range": Kmean_img_range
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
    range_dict = {}
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
            list_Info = []
             ##range logics
            min_val = data[field].min()
            max_val = data[field].max()
            bin_width = (max_val - min_val) / 7
            bins = [min_val + i * bin_width for i in range(8)]
            # 定义标签
            labels = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}' for i in range(7)]
            # 分组
            data['bin_group'] = pd.cut(data[field], bins=bins, labels=labels, include_lowest=True)
            data['bin_group'] = data['bin_group'].fillna(method='ffill')
            # 计算每个区间的中位数
            group_medians = data.groupby('bin_group')[y_field].median().reset_index()
            # 添加区间的中点
            group_medians['bin_midpoint'] = group_medians['bin_group'].apply(
            lambda x: (float(x.split('-')[0]) + float(x.split('-')[1])) / 2)
            # 按X轴中点排序
            #group_medians = group_medians.sort_values(by='bin_midpoint')
            n, bins, patches = ax.hist(data[field], bins=20, alpha=0.5, label=field, density=True, color=colors[i])

            ax.hist(data[field], bins=20, alpha=0.5, label=field, density=True, color=colors[i])
            ax.set_title(f'Distribution of {field}')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()
            #x_range_point = group_medians['bin_midpoint']
            #y_range_point = group_medians[y_field]
            #range_dict[field] = {
            #    'x_range_point': x_range_point,
            #    'y_range_point': y_range_point
            #}
            
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            
            for count in n:
                list_Info.append(count)
            x_ticks = ax.get_xticks()
            y_ticks = ax.get_yticks()
            range_dict[field] = {
                'x_range_point': x_ticks,
                'y_range_point': y_ticks,
                'group': list_Info
            }
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
    return img_base64 ,file_path, range_dict


def generate_scatter_plot(data, analysis_results,id_path):
    # 图片存储地址
    output_path = 'graph_place/graph_scatter'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    #numeric_columns = data.select_dtypes(include='number').columns

    # unpacked xyfields
    range_dict = {}  
    y_field = analysis_results['xy_fields']['y']
    x_fields = analysis_results['xy_fields']['x'].split(', ')
    
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
            ##range logics
            min_val = data[x_field].min()
            max_val = data[x_field].max()
            bin_width = (max_val - min_val) / 7
            bins = [min_val + i * bin_width for i in range(8)]
            # 定义标签
            labels = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}' for i in range(7)]
            # 分组
            data['bin_group'] = pd.cut(data[x_field], bins=bins, labels=labels, include_lowest=True)
            data['bin_group'] = data['bin_group'].fillna(method='ffill')
            # 计算每个区间的中位数
            group_medians = data.groupby('bin_group')[y_field].median().reset_index()
            # 添加区间的中点
            group_medians['bin_midpoint'] = group_medians['bin_group'].apply(
            lambda x: (float(x.split('-')[0]) + float(x.split('-')[1])) / 2)
            # 按X轴中点排序
            group_medians = group_medians.sort_values(by='bin_midpoint')
            
            ax.scatter(data[x_field], data[y_field], color=colors[i], edgecolor='black', alpha=0.7, label=x_field)
            ax.set_title(f'Scatter Plot of {x_field} vs {y_field}')
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            ax.legend()
            x_ticks = ax.get_xticks()
            y_ticks = ax.get_yticks()
            range_dict[x_field] = {
                'x_range_point': x_ticks,
                'y_range_point': y_ticks,
                'group': data['bin_group']
            }

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
    return img_base64 ,file_path, range_dict


def generate_chart_customized(data):
    pass




def generate_line_chart(data, analysis_results,id_path):
    # 图片存储地址
    output_path = 'graph_place/graph_line'
    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # 获取数值列
    # unpacked xyfields
     
    y_field = analysis_results['xy_fields']['y']
    x_fields = analysis_results['xy_fields']['x'].split(', ')
    
    #validate fields
    valid_x_fields = [field for field in x_fields if field in data.columns]
    if not valid_x_fields or y_field not in data.columns:
        raise ValueError("Invalid fields provided.")
    
    # 动态分组并计算中位数
    # 开始动态分组并计算中位数
    range_dict = {} 
    #color mapping
    cmap = cm.get_cmap('tab20', len(x_fields))  
    colors = [cmap(i) for i in range(len(x_fields))]
    
    # Scatter plots for each X field
    num_plots = len(valid_x_fields)
    fig, axs = plt.subplots(nrows=1, ncols=num_plots, figsize=(10 * num_plots, 6))

    for i, x_field in enumerate(valid_x_fields):
        ax = axs if num_plots == 1 else axs[i]
        if x_field in data.columns and y_field in data.columns:
            min_val = data[x_field].min()
            max_val = data[x_field].max()
            bin_width = (max_val - min_val) / 7
            bins = [min_val + i * bin_width for i in range(8)]
            # 定义标签
            labels = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}' for i in range(7)]
            # 分组
            data['bin_group'] = pd.cut(data[x_field], bins=bins, labels=labels, include_lowest=True)
            data['bin_group'] = data['bin_group'].fillna(method='ffill')
            # 计算每个区间的中位数
            group_medians = data.groupby('bin_group')[y_field].median().reset_index()
            # 添加区间的中点
            group_medians['bin_midpoint'] = group_medians['bin_group'].apply(
            lambda x: (float(x.split('-')[0]) + float(x.split('-')[1])) / 2)
            # 按X轴中点排序
            group_medians = group_medians.sort_values(by='bin_midpoint')
            # 结束动态分组并计算中位数
            # 生成折线图

            ax.plot(group_medians['bin_midpoint'], group_medians[y_field], marker='o', linestyle='-', color='blue')
            ax.set_title(f'Line Chart of {x_field} vs {y_field}')
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            ax.legend()
            x_range_point = group_medians['bin_midpoint']
            y_range_point = group_medians[y_field]
            x_ticks = ax.get_xticks()
            y_ticks = ax.get_yticks()
            range_dict[x_field] = {
                'x_range_point': x_range_point,
                'y_range_point': y_range_point,
                'x_label': x_ticks,
                'y_label': y_ticks,
                'group': data['bin_group']
            }       
            
            
    plt.tight_layout()

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    filename = f'line_chart_{timestamp}.png'

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
    
    
    return img_base64 ,file_path, range_dict
def generate_line_Kbean_chart(data, analysis_results,id_path):
    # 图片存储地址
    output_path = 'graph_place/graph_line'
    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # unpacked xyfields
     
    y_field = analysis_results['xy_fields']['y']
    x_fields = analysis_results['xy_fields']['x'].split(', ')
    
    #validate fields
    valid_x_fields = [field for field in x_fields if field in data.columns]
    if not valid_x_fields or y_field not in data.columns:
        raise ValueError("Invalid fields provided.")
    
    range_dict = {} 
    #color mapping
    cmap = cm.get_cmap('tab20', len(x_fields))  
    colors = [cmap(i) for i in range(len(x_fields))]
    
    # plots for each X field
    num_plots = len(valid_x_fields)
    fig, axs = plt.subplots(nrows=1, ncols=num_plots, figsize=(10 * num_plots, 6))

    for i, x_field in enumerate(valid_x_fields):
        ax = axs if num_plots == 1 else axs[i]
        if x_field in data.columns and y_field in data.columns:
            
            # 使用K-means聚类
            kmeans = KMeans(n_clusters=5, random_state=0).fit(data[[x_field]])
            data['cluster'] = kmeans.labels_
            # 计算每个聚类的中位数
            cluster_medians = data.groupby('cluster')[[x_field, y_field]].median().reset_index()
            # 按X轴排序
            cluster_medians = cluster_medians.sort_values(by=x_field)
            # 生成折线图
            
            ax.plot(cluster_medians[x_field], cluster_medians[y_field], marker='o', linestyle='-', color='blue')
            ax.set_title(f'Line Chart(KMEANS) of {x_field} vs {y_field}')
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            ax.legend()
            x_range_point = cluster_medians[x_field]
            y_range_point = cluster_medians[y_field]
            range_dict[x_field] = {
                'x_range_point': x_range_point,
                'y_range_point': y_range_point
            }  
    plt.tight_layout()

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    filename = f'line_chart(Kmeans)_{timestamp}.png'

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
    return img_base64 ,file_path, range_dict
def generate_pie_chart(data, analysis_results,id_path):
    # 图片存储地址
    output_path = 'graph_place/graph_pie'
    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # unpacked xyfields
     
    y_field = analysis_results['xy_fields']['y']
    x_fields = analysis_results['xy_fields']['x'].split(', ')
    
    #validate fields
    valid_x_fields = [field for field in x_fields if field in data.columns]
    if not valid_x_fields or y_field not in data.columns:
        raise ValueError("Invalid fields provided.")
    
    range_dict = {} 
    #color mapping
    cmap = cm.get_cmap('tab20', len(x_fields))  
    colors = [cmap(i) for i in range(len(x_fields))]
    
    # plots for each X field
    num_plots = len(valid_x_fields)
    fig, axs = plt.subplots(nrows=1, ncols=num_plots, figsize=(10 * num_plots, 6))

    for i, x_field in enumerate(valid_x_fields):
        ax = axs if num_plots == 1 else axs[i]
        if x_field in data.columns and y_field in data.columns:
            column = x_field
            # 生成饼图
            sizes = data[column].value_counts()
            labels = sizes.index
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title(f'Pie Chart of {column}')
            ax.legend()
            x_range_point = sizes
            y_range_point = labels
            range_dict[x_field] = {
                'x_range_point': x_range_point,
                'y_range_point': y_range_point
            }  
    plt.tight_layout()

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    filename = f'Pie_Chart_{timestamp}.png'

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
    return img_base64 ,file_path, range_dict