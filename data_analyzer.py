

def correlation_analyze(df):

    correlations = df.corr()
    
    # avg_correlations for columns
    avg_correlations = correlations.mean(axis=1)
    response_variable = avg_correlations.idxmax()
    
    return response_variable, correlations  # + list of columns name
def analyze_data_general(data):

    if data is None:
        print("数据集为空")
        return None

    analysis_results = {}
    ### CALL API ###
    ### Img text(report/ sampling / DIY summary)
    
    #result = generate_report_general(quality_report, analysis_results)
    #Y  = result['Response Variable']
    
    numeric_columns = data.select_dtypes(include='number').columns
    for col in numeric_columns:
        analysis_results[col] = {
            'median': data[col].median(),
            'max': data[col].max(),
            'min': data[col].min(),
            'std_dev': data[col].std()
        }

    numeric_df = data.select_dtypes(include='number')
    response_variable, correlations = correlation_analyze(numeric_df)
    return analysis_results, response_variable, correlations


def analyze_data_customized(data):
    pass
