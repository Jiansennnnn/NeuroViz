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
    for key, value in analysis_results.items():
        report += f"{key.capitalize()}:\n"
        for stat, val in value.items():
            report += f"\t{stat.capitalize()}: {val}\n"

    return report


def generate_report_customized(quality_report, analysis_results):
    pass
