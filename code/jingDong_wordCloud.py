import jieba


jieba.load_userdict("userdict.txt")              # 自定义词典

# 创建停用词list


# 对评论内容进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = open('stop_words.txt',encoding='utf-8')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

inputs = open('中差评.txt', 'r', encoding='utf-8')
outputs = open('中差评分词.txt', 'w')
for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    outputs.write(line_seg + '\n')
    line = line.replace("长夜难眠", "长夜难明")
outputs.close()
inputs.close()
print('分词完毕')

# 词频统计
import jieba.analyse
from collections import Counter  # 词频统计

with open('中差评分词.txt', 'r', encoding='gb18030') as fr:
    data = jieba.cut(fr.read())
data = dict(Counter(data))

with open('中差评词频.txt', 'w', encoding='gb18030') as fw:  # 读入存储wordcount的文件路径
    for k, v in data.items():
        fw.write('%s, %d\n' % (k, v))
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 生成词云
with open('中差评词频.txt') as f:
    # 提取关键词
    data = f.read()
    keyword = jieba.analyse.extract_tags(data, topK=50, withWeight=False)
    wl = " ".join(keyword)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，一般路径
        font_path='C:/Windows/Fonts/SimHei.ttf',
        height=1200,
        width=1600,
        # 设置字体最大值
        max_font_size=300,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
    )

    myword = wc.generate(wl)  # 生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('京东中差评词云图.jpg')  # 把词云保存下

