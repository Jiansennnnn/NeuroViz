import numpy as np
import pandas as pd
from .QwenModel_Client import QwenClient

class DataAnalyzer:
    def __init__(self, data: pd.DataFrame, qwen_client):
        self.data = data
        self.qwen_client = qwen_client



    #获取dataframe中的所有字段及其数据类型
    def get_field_info(self) -> dict:
        field_info = self.data.dtypes.to_dict()
        return field_info



    # 从数据中选择N行作为数据
    def get_sample_data(self,n=10):
         sample_data=self.data.sample(n)
         return  sample_data



    #将数据交给模型从中选出适合进行统计分析的字段，并且选出X跟Y轴
    def select_statistical_fields(self):
        field_info = self.get_field_info()
        sample_data = self.get_sample_data()

        prompt = f"""
        字段信息：{field_info}
        样本数据：{sample_data.to_dict(orient='records')}
        请根据这些信息，推荐适合进行统计分析的字段和适合用作X轴和Y轴的字段。

        ### 输出格式要求
        1. **统计分析字段**：请列出适合进行统计分析的字段，并且类型一定为数字类型的字段。格式为 `统计分析字段: field1, field2, field3`。
        2. **Y轴字段**：请推荐一个适合用作Y轴(可用于统计分析方法的因变量)的字段，格式为 `Y轴字段: field1`。
        2. **X轴字段**：请推荐一个或多个适合用作X轴(可用于统计分析方法的自变量)的字段，格式为 `X轴字段: field2，field3，field4`。
        4. 在**统计分析字段**中返回的字段务必为数字类型，请通过我传输给你样本数据进行判断，可以是整数或者浮点。
        
        ** 请务必确保输出X轴字段和Y轴字段的字段与给定的字段信息列表中的字段名一致**
        
        ** 如果输出的X轴字段和Y轴字段的字段有包含由于特殊字符（如单引号 '）转义所出现的字符（例如' 被转义成了 \'），请务必保证最后输出时去掉此类转义字符。**

        
        ### 示例
        统计分析字段$: deposit, age， others
        X轴字段$: age
        Y轴字段$: deposit，others
        
        注意：请在response中的'统计分析字段'，'X轴字段'，'Y轴字段'三个字段后都加上符号$，且每行字段结尾出不需要加上符号$，例如： `X轴字段$: variable_A，variable_B,variable_C`
        
        请严格按照以上该要求输出结果
        """

        model_response = self.qwen_client.call_qwen_api(prompt)

        # 解析模型的响应
        response_text = model_response
        statistical_fields = []
        xy_fields = {}

        # 根据模型返回的响应来进行解析
        lines = response_text.split('\n')
        for line in lines:
            if "统计分析字段$" in line:
                statistical_fields = [field.strip() for field in line.split(":")[1].split(",")]
            elif "X轴字段$" in line:
                xy_fields['x'] = line.split(":")[1].strip()
            elif "Y轴字段$" in line:
                xy_fields['y'] = line.split(":")[1].strip()

        return statistical_fields, xy_fields


#! TO DO
#! Multi_factor analysis

#def select_Multi_factors_statistical_fields(self):




    #计算指定字段的描述性统计量
    def descriptive_statistics(self, fields):
        if fields is None:
            raise ValueError("该报表中缺少描述性统计字段")

        stats = self.data[fields].describe()

        # 添加中位数
        median = self.data[fields].median()
        stats.loc['median'] = median

        return stats

    #计算指定字段之间的相关系数矩阵
    def correlation_matrix(self, fields=None):
        if fields is None:
            fields = self.data.select_dtypes(include='number').columns
        
        # Compute correlation matrix
        corr_matrix = self.data[fields].corr()

        # Generate  star counts based on correlation values
        star_values = []
        for field in fields:
            # 计算平均相关性，排除字段本身的相关性
            avg_corr = corr_matrix[field].drop(index=field).abs().mean()
            # 将平均相关性映射到1-5的推荐值，确保星级在1~5
            star_count = max(1, min(5, int(avg_corr * 5)))
            star_values.append({"field": field, "star_count": star_count})
            
        return corr_matrix


def start_algorithm(xy_fields,corr_matrix):

    # Generate  star counts based on correlation values
    star_values = []
    # By x Field
    fields_x = xy_fields['x'].split(', ')
    fields_y = xy_fields['y'].split(', ')
    avg_dict = dict()
   
    avg_y = corr_matrix[fields_y].drop(index=fields_y).abs().mean()
    for field in fields_x:
        # 计算平均相关性，排除字段本身的相关性
        # avg_corr = corr_matrix[field].drop(index=fields_y)
        # 排除x字段本身以及x字段和y字段的相关性
        avg_corr_x = corr_matrix[field].drop(index=field).drop(index=fields_y).abs().mean()
        # 将x字段相关性放入avg_dict中
        avg_total = (avg_corr_x * 0.2) + (avg_y * 0.8)
        if 0< avg_total[0] < 0.2:
            avg_dict[field] = 1
        elif 0.2 <= avg_total[0] < 0.4:
            avg_dict[field] = 2
        elif 0.4 <= avg_total[0] < 0.6:
            avg_dict[field] = 3
        elif 0.6 <= avg_total[0] < 0.8:
            avg_dict[field] = 4
        elif 0.8 <= avg_total[0] < 1.0:
            avg_dict[field] = 5
        else:
            avg_dict[field] = 0
    return avg_dict

    

def analyze_data(data, qwen_client):
    analyzer = DataAnalyzer(data, qwen_client)
    statistical_fields, xy_fields = analyzer.select_statistical_fields()
    results = {
            "field_info": analyzer.get_field_info(),
            "sample_data": analyzer.get_sample_data(),
            "statistical_fields": statistical_fields,
            "xy_fields": xy_fields,
            "descriptive_statistics": analyzer.descriptive_statistics(statistical_fields),
            "correlation_matrix": analyzer.correlation_matrix(statistical_fields)
    }
    start_count = start_algorithm(xy_fields, results['correlation_matrix'])
    return results,start_count



def analyze_data_customized(data):
    pass


