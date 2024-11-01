from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
ttfFile = os.path.join(current_dir, 'Times New Roman.ttf')
pdfmetrics.registerFont(TTFont('Times New Roman',ttfFile))


class Graphs:
    # 绘制标题
    @staticmethod
    def draw_title(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'Times New Roman'      # 字体名
        ct.fontSize = 18            # 字体大小
        ct.leading = 50             # 行间距
        ct.textColor = colors.black     # 字体颜色
        ct.alignment = 1    # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    
    @staticmethod
    def draw_little_title(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'Times New Roman'  # 字体名
        ct.fontSize = 15  # 字体大小
        ct.leading = 30  # 行间距
        ct.textColor = colors.red  # 字体颜色
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    # 绘制普通段落内容
    @staticmethod
    def draw_text(text: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 获取普通样式
        ct = style['Normal']
        ct.fontName = 'Times New Roman'
        ct.fontSize = 12
        ct.wordWrap = 'CJK'     # 设置自动换行
        ct.alignment = 0        # 左对齐
        ct.firstLineIndent = 32     # 第一行开头空格
        ct.leading = 25
        return Paragraph(text, ct)
    # 绘制表格
    @staticmethod
    def draw_table(args):
        # 列宽度
        col_width = [80] * len(args.columns)
        args_rounded = args.round(4)
        data = [args.columns.tolist()] + args_rounded.values.tolist()

        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times New Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table = Table(data, colWidths=col_width, style=style)
        return table
    # 创建图表
    @staticmethod
    def draw_bar(bar_data: list, ax: list, items: list):
        drawing = Drawing(500, 250)
        bc = VerticalBarChart()
        bc.x = 45       # 整个图表的x坐标
        bc.y = 45      # 整个图表的y坐标
        bc.height = 200     # 图表的高度
        bc.width = 350      # 图表的宽度
        bc.data = bar_data
        bc.strokeColor = colors.black       # 顶部和右边轴线的颜色
        bc.valueAxis.valueMin = 5000           # 设置y坐标的最小值
        bc.valueAxis.valueMax = 26000         # 设置y坐标的最大值
        bc.valueAxis.valueStep = 2000         # 设置y坐标的步长
        bc.categoryAxis.labels.dx = 2
        bc.categoryAxis.labels.dy = -8
        bc.categoryAxis.labels.angle = 20
        bc.categoryAxis.categoryNames = ax
        # 图示
        leg = Legend()
        leg.fontName = 'Times New Roman'
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 475         # 图例的x坐标
        leg.y = 240
        leg.dxTextSpace = 10
        leg.columnMaximum = 3
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(bc)
        return drawing
    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 15*cm        # 设置图片的宽度
        img.drawHeight = 8*cm       # 设置图片的高度
        return img
    
def ExportCore(Ideacontent,GcorrMatrix,CorrContent,GImg_path,Gjson_report):
    # 创建内容对应的空列表
    content = list()
    # 添加标题
    content.append(Graphs.draw_title('Data Analyst Report'))
    # 添加图片
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    
    Logo_target_path  = os.path.join('..', 'util', 'Logo_white.jpg')
    directory1 = os.path.normpath(os.path.join(current_dir, Logo_target_path))
    content.append(Graphs.draw_img(directory1))
    # 添加段落文字
    textintro = '''
    This document is based on the advanced analysis conducted by our NeuroViz (NV) product, aimed at providing readers with comprehensive insights into the dataset. We have employed a variety of analytical methods, including statistical descriptive analysis, variable distribution analysis, and correlation analysis, to reveal the underlying structure and characteristics of the data.

1. **Statistical Descriptive Analysis**: By quantifying key indicators within the dataset, we provide statistical information on central tendency and dispersion, suitable for initial data exploration and feature overview.

2. **Variable Distribution Analysis**: Utilizing graphical methods and statistical tests, we assess the distribution characteristics and skewness of each variable, enabling the identification of potential outliers and trends, thereby helping researchers understand the fundamental properties of the data.

3. **Correlation Analysis**: By calculating the correlation coefficients between variables, we uncover the relationships among them, providing a foundation for further modeling and prediction, making it applicable for exploratory data analysis and model optimization.

Through these analyses, we aim to equip readers with a thorough and in-depth understanding, facilitating greater value extraction in data-driven decision-making.
'''
    content.append(Graphs.draw_text(textintro))
    
    content.append(Graphs.draw_title(''))
    content.append(Graphs.draw_little_title('IDEA'))
    content.append(Graphs.draw_title(''))
    content.append(Graphs.draw_text(Ideacontent))
    
    
    
    
    content.append(Graphs.draw_title(''))
    content.append(Graphs.draw_little_title('Correlation Matrix Analysis'))
    # 添加表格
    GcorrMatrix
    content.append(Graphs.draw_table(GcorrMatrix))
    content.append(Graphs.draw_title(''))
    content.append(Graphs.draw_text(CorrContent))
    
    # 生成图表
    content.append(Graphs.draw_title(''))
    content.append(Graphs.draw_little_title('Distribution Analysis'))
    content.append(Graphs.draw_title(''))
    

    hist_img = GImg_path['histogram_img_path']
    scar_img = GImg_path['scatter_img_path']
    line_img = GImg_path['line_img_path']
    
    
    content.append(Graphs.draw_img(hist_img))
    content.append(Graphs.draw_img(scar_img))
    content.append(Graphs.draw_img(line_img))
    Gjson_report = str(Gjson_report)
    content.append(Graphs.draw_text(Gjson_report))
    
    current_file_path = os.path.abspath(hist_img)
    current_dir = os.path.dirname(current_file_path)
    PDF_Path = os.path.normpath(os.path.join(current_dir, 'report.pdf'))
    # 生成pdf文件
    doc = SimpleDocTemplate(PDF_Path, pagesize=letter)
    doc.build(content)
    
    return PDF_Path

