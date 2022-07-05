from pathlib import Path
import pandas as pd


# 获取当前目录下 有好评 中评 差评数据的txt
p = Path(r'D:\Learning\LPython\bigDataClass_2020Fall\paper_jingdong')
review_txt = list(p.glob('**/*.txt'))
all_data = pd.DataFrame()
for item in review_txt:
    emotion = item.stem     # 获取文件名 除后缀的部分
    with Path(item).open(mode='r',encoding='UTF-8') as f:
        con = f.read().split('\n')
    data = pd.DataFrame({'评论内容': con, '标签': [emotion] * len(con)})
    all_data = all_data.append(data)

all_data.to_excel('评论数据.xlsx', index=False)

from snownlp import SnowNLP
import pandas as pd
import re

# 读取数据
df = pd.read_excel('评论数据.xlsx', encoding='utf-8')
# print(df.info())
# 去掉空值的行
df = df.dropna(axis=0)
content = df['评论内容']

# 去除一些无用的字符   只提取出中文出来
#content = [' '.join(re.findall('[\u4e00-\u9fa5]+', item, re.S)) for item in content]
try:
    scores = [SnowNLP(i).sentiments for i in content]
except:
    print("被除数为零报错")
emotions = []
for i in scores:
    if i >= 0.75:
        emotions.append('好评')
    elif 0.45 <= i < 0.75:
        emotions.append('中评')
    else:
        emotions.append('差评')


df['情感分数'] = scores
df['情感'] = emotions
df.to_excel('NLP测试后数据.xlsx')

# 对比准确度
import pandas as pd

df = pd.read_excel('NLP测试后数据.xlsx')
# 看准确率   通过Snownlp情感打分 设置梯度得出的情感 好评 中评 差评 与实际标签相比较
data = df[df['标签'] == df['情感']]
print('总体准确率为：{:.3%}'.format(len(data) / len(df)))

data_good = df[24:527][df['标签'] == df['情感']]
print('好评准确率为：{:.3%}'.format(len(data_good) / len(df[24:527])))

data_mid = df[0:23][df['标签'] == df['情感']]
print('中评准确率为：{:.3%}'.format(len(data_mid) / len(df[0:23])))

data_bad = df[528:549][df['标签'] == df['情感']]
print('差评准确率为：{:.3%}'.format(len(data_bad) / len(df[528:549])))



