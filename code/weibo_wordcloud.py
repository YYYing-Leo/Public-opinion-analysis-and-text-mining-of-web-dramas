# coding=utf-8
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

import pandas as pd

# 数据
wb = pd.read_excel(r'D:\Learning\LPython\bigDataClass_2020Fall\paper_weibo\9.16开播-9.27结束_TFIDF关键词前100.xlsx')
data_wb = list(zip(wb['词语'],wb['重要性']))
#print(data_wb)

# 渲染图
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
        .add("", data_wb, word_size_range=[20, 85], shape='triangle-forward')  # SymbolType.ROUND_RECT
        .set_global_opts(title_opts=opts.TitleOpts(title='9.16-9.27 WordCloud词云'))
    )
    return c

# 生成图
wordcloud_base().render('9.16-9.27词云图.html')

