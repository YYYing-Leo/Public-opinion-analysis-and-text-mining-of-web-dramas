import requests
import pandas as pd
import zlib
import re
import time


def get_aiqiyi_danmu(tvid):
    """
    功能：给定tvid，获取爱奇艺一集的弹幕评论信息
    """
    # 建立空df
    df_all = pd.DataFrame()

    # 初始page_num
    page_num = 1

    while True:
        # 打印进度
        print(f'正在获取第{page_num}页的弹幕数据')

        try:
            # 获取URL
            url = f'https://cmts.iqiyi.com/bullet/{str(tvid)[-4:-2]}/{str(tvid)[-2:]}/{str(tvid)}_300_{page_num}.z'

            # 添加headers
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }

            # 发起请求
            try:
                r = requests.get(url, headers=headers, timeout=3)
            except Exception as e:
                print(e)
                r = requests.get(url, headers=headers, timeout=3)

            # 转换为arrry
            zarray = bytearray(r.content)

            # 解压字符串
            xml = zlib.decompress(zarray, 15 + 32).decode('utf-8')

            # 用户名
            name = re.findall('<name>(.*?)</name>', xml)
            # 评论ID
            contentId = re.findall('<contentId>(.*?)</contentId>', xml)
            # 评论信息
            content = re.findall('<content>(.*?)</content>', xml)
            # 展示时间
            showTime = re.findall('<showTime>(.*?)</showTime>', xml)
            # 点赞次数
            likeCount = re.findall('<likeCount>(.*?)</likeCount>', xml)

            # 保存数据
            df_one = pd.DataFrame({
                'name': name,
                'contentId': contentId,
                'content': content,
                'showTime': showTime,
                'likeCount': likeCount
            })

            # 循环追加
            df_all = df_all.append(df_one, ignore_index=True)

            # 休眠一秒
            time.sleep(1)

            # 页数+1
            page_num += 1

        except Exception as e:
            print(e)
            break

    return df_all


# 抓包获取视频tvid
tvid_list = [8928607238794800, 1633711019810300, 8520304822314600,
             2168755640240300, 8992780506613300, 2406998896996700,
             6095357464723600, 1664193322029900, 4568835856548000,
             2473578662358100, 3822019452341300, 2827333801193900]

episodes_list = ['第一集 张超强闯地铁站', '第二集 张晓倩收到匿名信', '第三集 张晓倩收到匿名信',
                 '第四集 严良再访李静', '第五集 江阳接连受到恐吓', '第六集 江阳朱伟开始走访',
                 '第七集 严良知晓爆炸原理', '第八集 侯贵平案实情曝光', '第九集 江阳得到重要线索',
                 '第十集 江阳遭污蔑索取贿赂', '第十一集 严良找到匿名寄信人', '第十二集 江阳死因揭秘']

# 循环获取所有集数据
for tvid, episodes in zip(tvid_list, episodes_list):
    print(tvid, episodes)
    # 获取数据
    df = get_aiqiyi_danmu(tvid=tvid)
    # 插入列
    df.insert(0, 'episodes', episodes)
    # 导出数据
    df.to_excel(f'aiqiyi_{episodes}.xlsx')