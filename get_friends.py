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

# 渲染好友分布地图
from pyecharts import Map

# @itchat.msg_register(itchat.content.TEXT)
# def print_content(msg):
#     print(msg['Text'])

itchat.auto_login(hotReload=True)
#itchat.run()
#itchat.send(u'aa测试消息发送', 'filehelper')
result = itchat.send('aa测试消息发送',  toUserName='bingoiloveu')
print(result)

friends = itchat.get_friends(update=True)
print(friends)
friends_df = pd.DataFrame(friends)
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
# plt.show()
provinces = friends_df['Province']
provinces.value_counts()
china_provinces = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东',
                   '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏',
                   '宁夏', '新疆', '香港', '澳门']
# 各省好友人数
value = [provinces.value_counts()[i] for i in china_provinces if i in provinces.unique()]
print(value)

# 好友分布省份
attr = [i for i in china_provinces if i in provinces.unique()]

print(attr)
map_wechat = Map("我的微信好友分布", width=1200, height=600)
map_wechat.add("", attr, value, maptype='china', is_visualmap=True, is_map_symbol_show=False)
print(len(attr))
print(len(value))
map_wechat.render()

map_wechat


# 获取好友UserName（不是昵称）列表
# user_names = friends_df['UserName']
# nb_friends = friends_df.shape[0]
# for i in tqdm(range(nb_friends)):
#     # 获取好友头像图片（base64编码）
#     img_data = itchat.get_head_img(userName=user_names[i])
#
#     # 另存为图片文件
#     with open('profiles/{}.jpg'.format(i), 'wb') as f:
#         f.write(img_data)

# ai.baidu.com开放平台API参数
# client_id =
# client_secret =
# token_r = requests.post('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret))
# token_r.json()
#
#
# # 将图片文件转码为base64
# def jpg2base64(file_name):
#     with open(file_name, 'rb') as f:
#         return base64.b64encode(f.read())