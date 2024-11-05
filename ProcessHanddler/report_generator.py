import pandas as pd
import numpy as np

def generate_report_general(quality_report, analysis_results):
    report = "Data Quality and Analysis Report:\n\n"

    # 数据质量报告
    if quality_report.get('missing_values'):
        report += "Missing Values:\n"
        for col, count in quality_report['missing_values'].items():
            report += f"\t{col}: {count} missing values\n"

    if quality_report.get('outliers'):
        report += "Outliers:\n"
        for col, outliers in quality_report['outliers'].items():
            report += f"\t{col}:\n"
            for outlier in outliers:
                report += f"\t\t{outlier}\n"

    # 统计分析报告
    report += "\nAnalysis Results:\n"
    # 添加统计分析字段
    report += "统计分析字段:\n"
    for field in analysis_results['statistical_fields']:
        report += f" - {field}\n"

    # 添加X轴和Y轴字段
    report += "\nX轴字段: {}\n".format(analysis_results['xy_fields']['x'])
    report += "Y轴字段: {}\n".format(analysis_results['xy_fields']['y'])

    # 添加描述性统计
    report += "\n描述性统计:\n"
    for field, stats in analysis_results['descriptive_statistics'].items():
        report += f" - {field}:\n"
        for stat, value in stats.items():
            report += f"   - {stat}: {value}\n"

    # 添加相关系数矩阵
    report += "\n相关系数矩阵:\n"
    for field, row in analysis_results['correlation_matrix'].items():
        report += f" - {field}:\n"
        for other_field, value in row.items():
            report += f"   - {other_field}: {value}\n"

    return report


def serialize_dict(data):
    if isinstance(data, dict):
        return {k: serialize_dict(v) for k, v in data.items()}
    elif isinstance(data, pd.Series) or isinstance(data, pd.Index) or isinstance(data, np.ndarray) or isinstance(data,  np.int64):
        return data.tolist()
    else:
        return data

def generate_report_Json_structured(quality_report, analysis_results):
    
    descriptive_statistics = {}
    for field, stats in analysis_results['descriptive_statistics'].items():
        descriptive_statistics[field] = {}
        for stat, value in stats.items():
            descriptive_statistics[field][stat] = value
    
    correlation_matrix = {}
    for field, row in analysis_results['correlation_matrix'].items():
        # Add the field as a key in the correlation_matrix dictionary
        correlation_matrix[field] = {}
        for other_field, value in row.items():
            correlation_matrix[field][other_field] = value
    
        
    report_Json_structured = {
        "title": "Data Quality and Analysis Report",
        "missing_values": serialize_dict(quality_report.get('missing_values',{})),
        "outliers": serialize_dict(quality_report.get('outliers',{})),
        "analysis_results": {
            "statistical_analysis_fields": serialize_dict(analysis_results['statistical_fields']),
            "x_axis_fields": [x.strip() for x in analysis_results['xy_fields']['x'].split(',')],
            "y_axis_field": analysis_results['xy_fields']['y'],
            "descriptive_statistics": serialize_dict(descriptive_statistics),
            "correlation_matrix": serialize_dict(correlation_matrix)
        }
    }
    
    return report_Json_structured
