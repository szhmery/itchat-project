import itchat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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