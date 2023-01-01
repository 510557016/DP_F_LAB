import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split

#大資料序需要一行一行讀進來
file = open('News_Category_Dataset.json','r',encoding='utf8')
data=[]
for line in file.readlines():
    dic =json.loads(line)
    data.append(dic)
df = pd.json_normalize(data)
df = df[['category','short_description']]
df.to_csv('all_dataset.csv',header = ['category', 'description'])

all_dataset_path = '/home/lenovo/DP/F_LAB/all_dataset.csv'
data_df = pd.read_csv(all_dataset_path,usecols = ['category','description'])
train_df, test_df = train_test_split(data_df, test_size=0.2)
train_df.to_csv('kaggle_train_dataset.csv')
test_df.to_csv('kaggle_test_dataset.csv')


#train_df = pd.read_csv(test_path,usecols = (['category','description']))
#train_df.dropna(inplace=True)
#train_df.sort_values(by=['category','description'],ascending=True)
#train_df.columns=['y','text']
#print(np.any(train_df.isnull())==True) 
#train_df.to_csv('spark_train_data.csv',header = ['y', 'text'])

#print(train_df.head(50))
