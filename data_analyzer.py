import pandas as pd
from QwenModel_Client import QwenClient

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
        2. **X轴字段**：请推荐一个适合用作X轴的字段，格式为 `X轴字段: field1`。
        3. **Y轴字段**：请推荐一个适合用作Y轴的字段，格式为 `Y轴字段: field2`。
        4. 在**统计分析字段**中返回的字段务必为数字类型，请通过我传输给你样本数据进行判断，可以是整数或者浮点。
        
        
        
        ### 示例
        统计分析字段$: deposit, age
        X轴字段$: age
        Y轴字段$: deposit
        
        注意：请在response中的'统计分析字段'，'X轴字段'，'Y轴字段'三个开头后都加上符号$，以便我能准确截取字符串
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
        return self.data[fields].corr()

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
    return results



def analyze_data_customized(data):
    pass


