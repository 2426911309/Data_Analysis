import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Pie, Bar, Line, Radar, WordCloud, Scatter, Page, Tab

# 读取数据
df = pd.read_csv('宜宾处理之后.csv', encoding='utf-8')

# 饼图
def drawPie(df):
    y_data = []
    df1 = df[(df['价格'] >= 0) & (df['价格'] <= 50)]
    y_data.append(len(df1))
    df2 = df[(df['价格'] >= 51) & (df['价格'] <= 100)]
    y_data.append(len(df2))
    df3 = df[(df['价格'] >= 101) & (df['价格'] <= 150)]
    y_data.append(len(df3))
    df4 = df[(df['价格'] >= 151) & (df['价格'] <= 200)]
    y_data.append(len(df4))
    df5 = df[(df['价格'] >= 201)]
    y_data.append(len(df5))
    x_data = ["0-50W", "51W-100W", "101W-150W", "151W-200W", "大于200W"]
    pie = (
        Pie()
        .add("", [list(z) for z in zip(x_data, y_data)])
        .set_global_opts(title_opts=opts.TitleOpts(title="宜宾房价价格区间统计"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

# 柱状图
def drawBar(df):
    df3 = df['房屋朝向'].value_counts()[:8]
    areaX = df['房屋朝向'].value_counts().index.tolist()[:8]
    areaY = [i for i in df3]
    bar = Bar()
    bar.add_xaxis(areaX)
    bar.add_yaxis("房屋朝向统计", areaY)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="房屋朝向统计"))
    return bar

# 折线图
def drawLine(df):
    df2 = df['小区'].value_counts()[:5]
    name = df['小区'].value_counts().index.tolist()[:5]
    data = [i for i in df2]
    line = Line()
    line.add_xaxis(name)
    line.add_yaxis("小区房源数量统计", data)
    line.set_global_opts(title_opts=opts.TitleOpts(title="前五小区房源数折线图"))
    return line

# 雷达图
def drawRadar(df):
    df3 = df['房屋朝向'].value_counts()
    areaX = df['房屋朝向'].value_counts().index.tolist()
    areaY = [i for i in df3]
    info = {areaX[i]: areaY[i] for i in range(len(areaX))}
    houseCount = []
    directionList = ['东', '东北', '东南', '北', '南', '西', '西北', '西南']
    for i in directionList:
        houseCount.append(info.get(i, 0))
    priceList = []
    df_grouped = df.groupby("房屋朝向")["价格"].mean()
    for index, row in df_grouped.items():
        if index in directionList:
            priceList.append(int(row))
    c_schema = [{"name": i} for i in directionList]
    radar = (
        Radar()
        .add_schema(schema=c_schema, shape="circle")
        .add("房屋朝向/房源数", [houseCount], color="red")
        .add("均价/万元", [priceList], color="blue")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="房屋朝向价格雷达图"))
    )
    return radar

# 词云图1（房屋朝向）
def drawWordCloud(df):
    df3 = df['房屋朝向'].value_counts()
    areaX = df['房屋朝向'].value_counts().index.tolist()
    data = [(areaX[i], str(df3.iloc[i])) for i in range(len(df3))]
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(series_name='房屋朝向词云图', data_pair=data, word_size_range=[20, 100], shape='pentagon')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='房屋朝向词云图', title_textstyle_opts=opts.TextStyleOpts(font_size=30)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud

# 词云图2（小区）
def drawWordCloud2(df):
    df3 = df['小区'].value_counts()
    areaX = df['小区'].value_counts().index.tolist()
    data = [(areaX[i], str(df3.iloc[i])) for i in range(len(df3))]
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add(series_name='小区词云图', data_pair=data, word_size_range=[20, 100], shape='diamond')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='小区词云图', title_textstyle_opts=opts.TextStyleOpts(font_size=30)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud

# 散点图
def drawScatter(df):
    two = df[['面积', '价格']].head(100)
    data = [[row["面积"], row["价格"]] for index, row in two.iterrows()]
    data.sort(key=lambda x: x[0])
    x_data = [d[0] for d in data]
    y_data = [d[1] for d in data]
    scatter = (
        Scatter()
        .add_xaxis(x_data)
        .add_yaxis(
            series_name="面积与价格",
            y_axis=y_data,
            symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="面积与价格散点图",
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
    )
    return scatter

# 创建一个Tab页面
tab = Tab()
tab.add(drawPie(df), "宜宾房价统计")
tab.add(drawBar(df), "房屋朝向统计图")
tab.add(drawLine(df), "前五小区房源数折线图")
tab.add(drawRadar(df), "房屋朝向与价格与房源雷达图")
tab.add(drawWordCloud(df), "房屋朝向词云图")
tab.add(drawWordCloud2(df), "小区词云图")
tab.add(drawScatter(df), "面积-价格散点图")

# 渲染到HTML文件
tab.render("宜宾二手房房价房源数据分析与可视化.html")