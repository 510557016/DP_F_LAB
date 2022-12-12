import pandas as pd
import json

#大資料序需要一行一行讀進來
file = open('News_Category_Dataset.json','r',encoding='utf8')
data=[]
for line in file.readlines():
    dic =json.loads(line)
    data.append(dic)
df = pd.json_normalize(data)
df = df[['category','short_description']]
df.to_csv('train_data.csv',header = ['category', 'description'])