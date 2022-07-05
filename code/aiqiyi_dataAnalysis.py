import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os
from wordcloud import WordCloud
import jieba

file_dir="./Danmu/"
# 获取文件名
files=[files for root,dirs,files in os.walk(file_dir)]

# 去重
def duplicate(files):
    for file in files:
        df = pd.read_csv(file_dir + file,encoding="utf-8-sig",index_col=0)
        data = df.drop_duplicates(subset=['DM_id'], keep='first')
        data.to_csv(file_dir + file,encoding='utf-8-sig',index=True,index_label="")
    print("去重完毕")

# 每一期弹幕总数的变化折线图
def danmuSumPlot(files):
    print("弹幕总数变化图绘制中...")
    list1 = ['110','111','112','113','114','115','116','117','118','119','120','121','122','123','124']
    data_sum=[]
    for file in files:
        data = pd.read_csv(file_dir + file,encoding="utf-8-sig",index_col=0)
        data_sum.append(len(data))

    matplotlib.rcParams["font.family"] = "SimHei"
    plt.plot(list1, data_sum, "c")
    plt.ylabel("弹幕数")
    plt.xlabel("《睡前消息》期数")
    plt.title("每一期弹幕总数的变化图")
    plt.savefig('./Analysis/弹幕总数变化图', dpi=600)
    plt.show()
    print("绘制完毕")

# 发弹幕总数TOP10的用户柱状图
def danmuUserTopBarh(files):
    print("弹幕TOP10用户图绘制中...")
    datas=[]
    for file in files:
        datas.append(pd.read_csv(file_dir + file,encoding="utf-8-sig",index_col=0))

    # 先合并全部csv文件，再进行统计
    data=pd.concat(datas)
    data = data.groupby('DM_userID').size().reset_index(name="count")
    data = data.sort_values("count", ascending=False)

    label = []  # y轴的值
    width = []  # 给出具体每个直方图的数值
    i = 0

    for item in data.values:
        if i < 10:
            label.append(item[0])
            width.append(item[1])
            i += 1
        else:
            break

    matplotlib.rcParams["font.family"] = "SimHei"
    y = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # 给出在y轴上的位置
    plt.barh(y=y, width=width, tick_label=label)  # 绘制水平直方图
    plt.ylabel("用户ID")
    plt.xlabel("弹幕数")
    plt.title("发弹幕总数TOP10的用户柱状图")
    plt.subplots_adjust(left=0.17)  # 控制图片左边的间隔  避免显示不全
    plt.savefig('./Analysis/TOP10', dpi=600, left=0.17)
    print("绘制完毕")

# 每期弹幕密度变化图
def danmuDensityChange(files):
    print("弹幕密度变化图绘制中...")
    sets=110
    for file in files:
        data = pd.read_csv(file_dir + file, encoding="utf-8-sig", index_col=0)
        data = data.sort_values("DM_time")

        # 先对弹幕发送时间进行取整
        data['DM_time'] = [int(item) for item in data.DM_time]
        data = data.groupby('DM_time').size().reset_index(name="counted")

        list2 = [item for item in data.DM_time]
        data_sum = [item for item in data.counted]
        matplotlib.rcParams["font.family"] = "SimHei"
        plt.plot(list2, data_sum, "c")
        plt.ylabel("弹幕数量")
        plt.xlabel("视频时间轴/(秒)")
        plt.title(str(sets)+"期弹幕密度变化图")
        plt.savefig("./Analysis/弹幕密度变化/"+str(sets)+'期弹幕密度变化图', dpi=600)
        sets+=1
    print("绘制完毕")

# 每期的弹幕词云
def danmuWordCloud(files):
    print("弹幕词云绘制中...")
    sets = 110
    for file in files:
        data = pd.read_csv(file_dir + file, encoding="utf-8-sig", index_col=0)
        # 先把全部弹幕信息写成一个字符串，再调用方法
        words = ''
        for item in data.DM_text:
            words += item

        words=" ".join(jieba.cut(words))
        # 这个scale参数是画布大小参数，也就是调整分辨率的，10代表是原来的10倍大小，越高分辨率越高
        wd = WordCloud(font_path='simhei.ttf', max_words=40, background_color='white',min_font_size=10,scale=10).generate(words)
        plt.imshow(wd)
        plt.axis("off")
        wd.to_file("./Analysis/词云/第" + str(sets) + "期词云.jpg")
        sets+=1
    print("绘制完毕")


if __name__ == '__main__':
    # 去重
    duplicate(files[0])

    # 每一期弹幕总数的变化折线图
    danmuSumPlot(files[0])

    # 发弹幕总数TOP10的用户柱状图
    danmuUserTopBarh(files[0])

    # 每期弹幕密度变化图
    danmuDensityChange(files[0])

    # 每期的弹幕词云
    danmuWordCloud(files[0])
