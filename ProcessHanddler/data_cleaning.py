
# 对数据异常值进行处理，将数据类型出现最多次数的值填充

def handle_missing_and_outliers(data):
    # 分离数值类型和非数值类型列
    numeric_columns = data.select_dtypes(include='number').columns
    non_numeric_columns = data.select_dtypes(exclude='number').columns
    
    # 用出现最多的值填充空值
    for column in non_numeric_columns:
        if data[column].isna().any():
            mode_value = data[column].mode()[0]
            data[column].fillna(mode_value, inplace=True)

    # 用中位数填充数值类型列的空值
    for column in numeric_columns:
        if data[column].isna().any():
            median_value = data[column].median()
            data[column].fillna(median_value, inplace=True)
    data[numeric_columns] = data[numeric_columns].astype('float64')

    # 用中位数填充离群值
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