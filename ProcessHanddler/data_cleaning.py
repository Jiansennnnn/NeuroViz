
# 对数据异常值进行处理，将数据类型出现最多次数的值填充

def handle_missing_and_outliers(data):
    # 用出现最多的值填充空值
    for column in data.columns:
        if data[column].isna().any():
            mode_value = data[column].mode()[0]
            data[column].fillna(mode_value, inplace=True)

    # 用中位数填充离群值
    numeric_columns = data.select_dtypes(include='number').columns
    for col in numeric_columns:
        q_low = data[col].quantile(0.01)
        q_hi = data[col].quantile(0.99)
        median = data[col].median()
        outlier_condition = (data[col] < q_low) | (data[col] > q_hi)
        data.loc[outlier_condition, col] = median

    data = data.infer_objects()

    return data

def data_cleaning_customized(data):
#是否可以根据AI对异常数据进行识别，并进行填充。在quality check 里面，利用聚类方法或回归模型预测合理的正常值，并进行替换异常值
    pass