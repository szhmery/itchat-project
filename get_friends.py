import itchat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 渲染好友分布地图
from pyecharts import Map

# @itchat.msg_register(itchat.content.TEXT)
# def print_content(msg):
#     print(msg['Text'])

itchat.auto_login(hotReload=True)
#itchat.run()
#itchat.send(u'aa测试消息发送', 'filehelper')
result = itchat.send('aa测试消息发送',  toUserName='smallpengll')
print(result)

friends = itchat.get_friends(update=True)
print(friends)
friends_df = pd.DataFrame(friends)
friends_df.head()
friends_df.info()
friends_df['Sex'].value_counts()
sex_counts = friends_df['Sex'].value_counts().values
plt.pie(sex_counts, explode=(0,0.1,0), shadow=True, autopct='%1.1f%%', startangle=90)
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
map_wechat.render()
print(map_wechat)