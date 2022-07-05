# coding=utf-8
import jieba
import jieba.analyse
import re
import time
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType


#------------------------------------中文分词------------------------------------
jieba.load_userdict("userdict.txt")              # 自定义词典
#jieba.suggest_freq('紫金陈', True)
jieba.analyse.set_stop_words('stop_words.txt')   # 停用词词典


cut_words = ""
all_words = ""
f = open('aiqiyi_jiangyang_fenci.txt', 'w',encoding='utf-8')
for line in open('aiqiyi_jiangyang.txt', encoding='utf-8'):
    line.strip('\n')
    seg_list = jieba.cut(line,cut_all=False)  #精确模式
    #print(" ".join(seg_list))
    #f.write(" ".join(seg_list))
    cut_words = (" ".join(seg_list))
    all_words += cut_words
else:
    f.close()

# 输出结果
all_words = all_words.split()
#print(all_words)


#词频统计
c = Counter()
for x in all_words:
    if len(x)>1 and x != '\r\n':
        c[x] += 1

#输出词频最高的前10个词
#print('\n词频统计结果：')
words = []
for (k,v) in c.most_common(100):
    # print(k, v)
    words.append((k,v))
    #print("%s:%d"%(k,v))

# 渲染图
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape='diamond')
        .set_global_opts(title_opts=opts.TitleOpts(title='江阳/白宇词云图'))
    )
    return c

# 生成图
wordcloud_base().render('江阳词云图.html')