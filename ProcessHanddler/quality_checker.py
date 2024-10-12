def check_quality(data):
    quality_report = {
        'missing_values': {},
        'outliers': {}
    }

    # 检查缺失值
    for column in data.columns:
        missing_count = data[column].isna().sum()
        if missing_count > 0:
            quality_report['missing_values'][column] = missing_count

    # 检查异常值
    numeric_columns = data.select_dtypes(include='number').columns
    for col in numeric_columns:
        q_low = data[col].quantile(0.01)
        q_hi = data[col].quantile(0.99)
        outliers = data[(data[col] < q_low) | (data[col] > q_hi)][col]
        if len(outliers) > 0:
            quality_report['outliers'][col] = outliers.tolist()

    return quality_report
