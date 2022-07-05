# coding=utf-8 
import os
import pandas as pd
import numpy as np
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties

#------------------------------------中文分词------------------------------------
jieba.load_userdict("userdict.txt")              # 自定义词典
#jieba.suggest_freq('紫金陈', True)
jieba.analyse.set_stop_words('stop_words.txt')   # 停用词词典

cut_words = ""
#all_words = ""
f = open('9.15定档-9.16开播_分词.txt', 'w', encoding='utf-8')
for line in open('9.15定档-9.16开播_去重964.txt', encoding='utf-8'):
    line.strip('\n')
    seg_list = jieba.cut(line,cut_all=False)  #精确模式
    #print(" ".join(seg_list))
    f.write(" ".join(seg_list))
    #cut_words = (" ".join(seg_list))
    #all_words += cut_words
else:
    f.close()


# # 数据清洗 txt文件按行去重
# list01 = []
# for i in open('9.16开播_分词.txt', encoding='utf-8'):
#     if i in list01:
#         continue
#     list01.append(i)
# with open('9.16开播_分词_去重.txt', 'w', encoding='utf-8') as handle:
#     handle.writelines(list01)

# 提取主题词 返回的词频其实就是TF-IDF
keywords = jieba.analyse.extract_tags(cut_words,
                                      topK=100,
                                      withWeight=True,
                                      allowPOS=('a','e','n','nr','ns', 'v')) #词性 形容词 叹词 名词 动词

# 以列表形式返回
print(keywords)

# 数据存储
pd.DataFrame(keywords, columns=['词语','重要性']).to_excel('9.16开播-9.27结束_TFIDF关键词前100.xlsx')

# keyword本身包含两列数据
ss = pd.DataFrame(keywords,columns = ['词语','重要性'])     
# print(ss)

#------------------------------------数据可视化------------------------------------



plt.figure(figsize=(10,6))
plt.title('9.16-9.27 TF-IDF Ranking')
fig = plt.axes()
plt.xticks(fontsize=10)  #坐标轴字体大小
plt.yticks(fontsize=10)
plt.barh(range(len(ss.重要性[:25][::-1])),ss.重要性[:25][::-1])
fig.set_yticks(np.arange(len(ss.重要性[:25][::-1])))
font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')
fig.set_yticklabels(ss.词语[:25][::-1],fontproperties=font)
fig.set_xlabel('Importance')
plt.show()
     


