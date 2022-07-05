#coding: utf-8
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import sys
import codecs
import importlib
importlib.reload(sys)

#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


#---------------------  第一步 读取数据(已分词)  ----------------------
corpus = []


# 读取预料 一行预料为一个文档
for line in open('9.15定档-9.16开播_分词.txt', 'r', encoding='utf-8').readlines():
    corpus.append(line.strip())

        
#-----------------------  第二步 计算TF-IDF值  ----------------------- 
# 设置特征数
n_features = 500


tf_vectorizer = TfidfVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words=['沉默','white','真相','我要','想到','看到','看起来',
                                            '可以','微博','比较','这里','视频','真的','一个',
                                            '自己','两集','同事','沉真','老师','没有','时候',
                                            '为了','他们','什么','全文','收起','我们','知道',
                                            '不是','就是','这样','有人','怎么','这个','那个',
                                            '这部','有点','那么','白宇','by','下三土','江阳',
                                            '微博','微博','微博','微博',],
                                max_df = 0.8,
                                min_df = 0.002) #去除文档内出现几率过大或过小的词汇

tf = tf_vectorizer.fit_transform(corpus)

print(tf.shape)
print(tf)

#-------------------------  第三步 LDA分析  ------------------------ 
from sklearn.decomposition import LatentDirichletAllocation

# 设置主题数
n_topics = 3

lda = LatentDirichletAllocation(n_components=n_topics,
                                max_iter=100,
                                learning_method='online',
                                learning_offset=50,
                                random_state=0)
lda.fit(tf)

# 显示主题数 model.topic_word_
print(lda.components_)
# 几个主题就是几行 多少个关键词就是几列 
print(lda.components_.shape)                         

# 计算困惑度
print(u'困惑度：')
print(lda.perplexity(tf,sub_sampling = False))

# 主题-关键词分布
def print_top_words(model, tf_feature_names, n_top_words):
    for topic_idx,topic in enumerate(model.components_):  # lda.component相当于model.topic_word_
        print('Topic #%d:' % topic_idx)
        print(' '.join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
        print("")

# 定义好函数之后 暂定每个主题输出前20个关键词
n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()
# 调用函数
print_top_words(lda, tf_feature_names, n_top_words)




#------------------------  第四步 可视化分析  ------------------------- 
import pyLDAvis
import pyLDAvis.sklearn

#pyLDAvis.enable_notebook()

data = pyLDAvis.sklearn.prepare(lda,tf,tf_vectorizer)
#print(data)


#显示图形
pyLDAvis.show(data)
#pyLDAvis.display(data)
#pyLDAvis.save_json(data,'9.15_lda_2.html')
