#coding=utf8
import itchat
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm
import requests
import base64
import time

# 渲染好友分布地图
from pyecharts import Map
import jieba
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from matplotlib.font_manager import FontProperties

SIGNATURES = 1
HEAD = 0
PROVINCE = 1
# @itchat.msg_register(itchat.content.TEXT)
# def print_content(msg):
#     print(msg['Text'])

itchat.auto_login(hotReload=True)
#itchat.run()
#itchat.send(u'aa测试消息发送', 'filehelper')
result = itchat.send('aa测试消息发送',  toUserName='filehelper')

friends = itchat.get_friends(update=True)
friends_df = pd.DataFrame(friends)


if PROVINCE is 1:
    friends_df.head()
    friends_df.info()
    friends_df['Sex'].value_counts()
    labels = [u'male',u'female',u'null']
    sex_counts = friends_df['Sex'].value_counts().values
    print(sex_counts)
    plt.pie(sex_counts, explode=(0,0.1,0), labels=labels, shadow=True, autopct='%1.1f%%', startangle=90)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.show()
    provinces = friends_df['Province']

    ## 全部好友省份分部
    p_value = provinces.value_counts()
    print(p_value)
    site = []
    statistics = []
    for i,v in p_value.items():
        print('province: ',i,'count: ',v)
        site.append(i)
        statistics.append(v)
    print(site, len(site))
    print(statistics,len(statistics))

    ## 中国省份人数分部
    china_provinces = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东',
                       '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏',
                       '宁夏', '新疆', '香港', '澳门']
    # 各省好友人数
    value = [provinces.value_counts()[i] for i in china_provinces if i in provinces.unique()]
    print(value)

    print(provinces.unique())
    # 好友分布省份
    attr = [i for i in china_provinces if i in provinces.unique()]

    print(attr)
    map_wechat = Map("我的微信好友分布", width=1200, height=600)
    #map_wechat.add("", site, statistics, maptype='world', is_visualmap=True, is_map_symbol_show=False)
    map_wechat.add("", attr, value, maptype='china', is_visualmap=True, is_map_symbol_show=False)
    print(len(attr))
    print(len(value))
    map_wechat.render()

    map_wechat

if HEAD is 1:
    # 获取好友UserName（不是昵称）列表
    user_names = friends_df['UserName']
    print(user_names)
    nb_friends = friends_df.shape[0]

    for i in tqdm(range(nb_friends)):
        # 获取好友头像图片（base64编码）
        img_data = itchat.get_head_img(userName=user_names[i])

        # 另存为图片文件
        with open('profiles/{}.jpg'.format(i), 'wb') as f:
            f.write(img_data)
            #print(format(i))

    # # 将图片文件转码为base64
    def jpg2base64(file_name):
        with open(file_name, 'rb') as f:
            return base64.b64encode(f.read())

    url = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/general?access_token=24.0210e6e5526b3c0d5747afcdc30fd425.2592000.1530952457.282335-11366325'

    categories = [0 for i in range(nb_friends)]
    print("categories:",categories)
    for i in tqdm(range(nb_friends)):
        response = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'image': jpg2base64('profiles/{}.jpg'.format(i))})

        try:
            categories[i] = response.json()['result'][0]['keyword']
            print(categories[i])
            #time.sleep(2)
            #break
        except (KeyError, TimeoutError):
            continue

categories=['工艺品', '阔叶树', '卡通动漫人物', '沿街店面', '狮子猫', '海洋', '卡通动漫人物', '工笔画', '人物特写', '文字图片', '人物特写', '小丸子', '中年男性', '玩具', '瓷器', '天空', '荨麻', '灯具', '草帽', '摩托车', '办公桌', '街道', '人物特写', '短靴', '人偶娃娃玩具', '城垣', '墙绘', '自然风景', '翠鸟', '卡通动漫人物', '加工车间', '卡通动漫人物', '喇叭裤', '屏幕截图', '书籍', '卡通动漫人物', '玩具', '白腿小隼', '场记板', '帽子', '人物特写', '借阅室', '衬衫', '天空', '香水', '树', '小丑鱼', '轿车', '二维码', '沿街店面', '商品标签', '面具', '猫', '袜子娃娃', '卡通动漫人物', '美女', '卡通动漫人物', '城市街道', '拉布拉多犬', '轿车', '婺源县', '体育场馆', '地板砖', '触控板', '卡通动漫人物', '会徽', '卡通动漫人物', '卡通动漫人物', '园林景观', '人物特写', '头发', '沙发', '眼镜', '卡通动漫人物', '屏幕截图', '牛仔衣', '美女', '人物特写', '建筑', '大象', '霞光', '美女', '旗帜', '小孩', 0, '婺源县', '桥梁', '玉器', '美女', '油画', '草原', '卡通婚纱照', '工笔画', '人物特写', '雕像', '天空', '婚纱写真', '手绘花', '建筑', '卡通动漫人物', '椅子', '汽车标志', '化妆舞会', '人偶娃娃', '油画', '帽子', '手机', '英语小报', '人物特写', '药品', '人物特写', '屏幕截图', '美女', '天空', '建筑', '人物特写', '海洋', '屏幕截图', '文字图片', '人物特写', '荧光壁纸', '健身运动', '文字图片', '漂泊信天翁', '摆花', '卡通动漫人物', '桨', '文字图片', '鹅卵石', '显示器屏幕', '商店商场', '人物特写', '人物特写', '小女孩', '海洋', '天空', '草原', '书法', '卡通动漫人物', '卡通动漫人物', '卡通动漫人物', '芒果', '天空', '卡通动漫人物', '草原', '工笔画', '秃鹰', '人偶娃娃玩具', '海洋', '雕像', '布偶猫', '狗娃花', '工笔画', '人脸', '美女', '婺源县', '小女孩', '卡通动漫人物', '卡通动漫人物', '游泳圈', '羊杂汤管', '人物特写', '男孩', '手镯', '会徽', '袋鼠', '男人', '卡通动漫人物', '卡通动漫人物', '城市街道', '日本樱花', '滑雪板', '民居', '图标', '喜玛拉雅兔', '卡通动漫人物', '男人', '金吉拉猫', '跳绳', '汽车方向盘', '盖毯', '沙发', '长城', '江河', '卡通动漫人物', '人物特写', '文字图片', '婚纱写真', '卡通动漫人物', '婚纱写真', '大象', '人物特写', '小丸子', '灰雁', '美女', '美女', '人物特写', '挎包手袋', '长凳', '人物特写', '公路', '俄罗斯蓝猫', '小丸子', '婺源县', '合照', '人物特写', '紫藤', '沙发', '包装袋/盒', '人物特写', '鸟类', '齿轮图', '箭靶', '卡通动漫人物', '校徽', '罗大佑', '人物特写', '芦花', '好莱坞', '工笔画', '卡通动漫人物', '湖泊', '人物特写', '汽车标志', '人物特写', '裤子', '合照', '门洞', '卡通动漫人物', '红果', '轿车', '树枝', '卡通动漫人物', '卡通动漫人物', '眼睛', '发膜', '卡通动漫人物', '商品标签', '油菜花', '巷道', '餐饮场所', '简笔画', '窗帘/窗纱', '合照', '小盆栽', '包', '豚鼠', '天空', '花卉', '玩具', '马尾辫', '苏俄猎狼', '徐州博物馆', '狗', '手绘花', '虫子', '海鸥图', '合照', '红嘴鸥', '滑雪图', '郁金香花', '桨', '山峦', '中年男性', '帽子', '卡通动漫人物', '油菜花', '蒙古马', '面具', '奖杯', '女孩', '古建筑', '街道', '小孩', '小孩', '玩具公仔', '公路', '脚', '徐州博物馆', '人物特写', '小孩', '纸风车', '天空', '婚纱写真', '体育场馆', '卡通动漫人物', '园林景观', '女人', '蚕桑', '屏幕截图', '卡通动漫人物', '雕像', '工笔画', '小黄人', '刮刀', '公路', '手枪速射', '卡通动漫人物', '书法', '工笔画', '稻谷', '纸壳人', '人物特写', '卡通动漫人物', '美女', '玩具', '湖泊', '格子衣', '建筑', 'NBA', '帽子', '太阳镜', '望谟崖摩', '树', '礼服', '骷髅头', '考洛丝', '人物特写', '铁路轨道', '猫', '薰衣草', '卡通动漫人物', '人物特写', '人物特写', '美女', '人物特写', '博美犬/松鼠犬', '人物特写', '工笔画', '花卉', '帽子', '人物特写', '小树林', '女孩', '人物特写', '格子衣', '树发藓', '婴儿', '卡通动漫人物', '薄公英', '卡通动漫人物', '趾甲', '小孩', '婚纱写真', '建筑', '山峦', '屏幕截图', '图标', '人物特写', '婺源县', '人物特写', '冰淇淋', '山鹃', '人物特写', '肌肉男', '头饰', '婺源县', '合照', '残雪', '卡通动漫人物', '简笔画', '海洋', '雕像', '睡衣', '扶郎', '眼镜蛇', '屏幕截图', '人物特写', '凤凰', '马尔济斯犬/玛尔基斯犬', '卡通动漫人物', '美女', '卡通动漫人物', '美女', '卡通动漫人物', '异国短毛猫', '军人', '手绘墙', '爆炸头', '女人', '摩托车', '卡通动漫人物', '人物特写', '挡珠', '新芽', '海洋', '城楼', '卡通动漫人物', '美女', '人物特写', '模糊图片', '人物特写', '卡通动漫人物', '婚纱写真', '中年男性', '领带', '樱桃', '楼阁', '美女', '胸针', '卡通动漫人物', '人物特写', '旗袍', '鲨鱼', '卡通动漫人物', '儿童', '车标', '美女', '手', '气球', '人物特写', '卡通娃娃', '园林景观', '峡谷', '海报宣传画', '建筑', '樱兰高校', '人物特写', '人物特写', '屏幕截图', '雕像', '儿童', '卡通动漫人物', '瑜伽', '人物特写', '懒猴', '建筑', '光头强', '天空', '美女', '爬雪山', '人物特写', '美女', '美女', '卡通动漫人物', '安达曼群岛蛇雕', '美女', '卡通动漫人物', '体育场馆', '工笔画', '气球', '法兰西斗牛犬', 't恤', '汽车标志', '人物特写', '帽子', '牛仔衣', '卡通动漫人物', '笔记本配件', '卡通动漫人物', '素描画', '黄山松', '卡通动漫人物', '路标', '人物特写', '卡通动漫人物', '人物特写', '男人', '铁人三项', '领结', '卡通动漫人物', '中年男性', '绘画', '卡通动漫人物', '小孩', '荧光壁纸', '盆栽植物', '儿童', '孟买猫', '小孩', '卡通动漫人物', '亲子装', '蓝色海豚', '人物特写', '黑猫', '卧室', '女孩', '海洋', '卡通动漫人物', '蓟花', '婴儿', '自然/人文景观', '图画', '狮子', '建筑', '卡通动漫人物', '香水', '雕像', '卡通动漫人物', '人物特写', '人物特写', '工笔画', '头发', '美女', '孟买猫', '人物特写', '屏幕截图', '玩具', '卡通动漫人物', '美女', '苏格兰折耳猫', '美女', '大象', '卡通动漫人物', '大象', '连衣裙', '女人', '宠物公园', '卡通图像', '卡通动漫人物', '商务套装', '工笔画', '女人', '人物特写', '抹胸', '日本秋田犬', '沙发', '椰树', '卡通动漫人物', '美女', '人物特写', '动物矢量图', '卡通动漫人物', '盖头', '工笔画', '长颈鹿', '工笔画', '灯笼花', '婺源县', '铁筷子', '美女', '美女', '产妇帽', '合照', '人脸', '街灯', '草帽', '卡通动漫人物', '人物特写', '红色玫瑰', '儿童', '街灯', '屏幕截图', '聪明的一休', '西服', '天空', '金吉拉猫', '人物特写', '闪电', '电烤箱', '屏幕截图', '波斯菊', '手', '盆栽植物', '女人', '面具', '风信子', '女人', '马里奥', '工笔画', '工笔画', '头发', '亲吻', '礼服', '屏幕截图', '卡通动漫人物', '屏幕截图', '卡通动漫人物', '宠物犬', '卷毛比熊犬', '美女', '八仙花', '螃蟹', '非洲象', '猫', '天空', '摩天轮', '美女', '卡通动漫人物', '婺源县', '花墙', '喇叭花', '美女', '手', '人物特写', '通灵王', '卡通动漫人物', '文字图片', 'T恤', '卡通动漫人物', '书法', '天空', '美女', '凤凰树', '古建筑', '美女', '落叶', '人脸', '儿童', '人物特写', '屏幕截图', '卡通动漫人物', '美女', '显示器屏幕', '人物特写', '礼服', '卡通动漫人物', '法兰西斗牛犬']
categories = pd.Series(categories)
print(categories)

## 设置font,标签可以显示中文
font = FontProperties(fname=r"/Users/zhaohsun/Documents/Work/Tech/python/itchat-project/simhei.ttf", size=14)  #size可不用指定
data = categories.value_counts()[categories.value_counts() > 5]
print(data)

labels = [label for label in data.index.values]
print(labels)
data.columns=[labels]

ax = data.plot(kind='bar')


ax.set_xticklabels(labels, fontproperties=font)
plt.show()


np.sum(categories.value_counts()[categories.value_counts() > 5])
categories.value_counts()[['人物特写', '美女', '男人', '人脸', '中年男性', '女人', '罗大佑', '婚纱写真', '合照']]
nb_photo = np.sum(categories.value_counts()[['人物特写', '美女', '男人', '人脸', '中年男性', '女人', '罗大佑', '婚纱写真', '合照']])
print(nb_photo)


if SIGNATURES is 1:
    # 获取好友签名
    signatures = friends_df['Signature'][friends_df['Signature'].isnull() == False]
    # 合并为字符串格式
    signature_text = ''.join(signatures)
    print(signature_text)
    # 使用结巴分词
    word_list = jieba.cut(signature_text, cut_all=True)
    word_space_split = ' '.join(word_list)
    print(word_space_split)
    # 生成词云
    coloring = np.array(Image.open("profiles/0.jpg"))
    stopwords = set(STOPWORDS) | {'span', 'class', 'emoji'}
    my_wordcloud = WordCloud(background_color="white", max_words=500,
                             mask=coloring, max_font_size=200, random_state=42, stopwords=stopwords,
                             font_path="simhei.ttf").generate(word_space_split)
    image_colors = ImageColorGenerator(coloring)

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1)

    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()