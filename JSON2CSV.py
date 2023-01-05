import pandas as pd
import numpy as np
import json
import regex
from sklearn.model_selection import train_test_split


def clean_text(text):
    text = regex.sub(r"@[A-Za-z0-9]+", ' ', text)
    text = regex.sub(r"https?://[A-Za-z0-9./]+", ' ', text)
    text = regex.sub(r"[^a-zA-z.!?'0-9]", ' ', text)
    text = regex.sub('\t', ' ',  text)
    text = regex.sub(r" +", ' ', text)
    return text


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

data_df.dropna(inplace=True)

#print("data_df size=",data_df.shape)

print("data_df size=",data_df.shape[0])

train_df, tmp_test_df = train_test_split(data_df, train_size=120000,test_size=int(data_df.shape[0])-120000,random_state=42)

train_df['category'] = train_df['category'].apply(clean_text) 
tmp_test_df['category'] = tmp_test_df['category'].apply(clean_text)

train_df.to_csv('kaggle_train_dataset_clear_text_120000.csv')

val_df, test_df = train_test_split(data_df, train_size=6000,test_size=6000,random_state=42)

val_df.to_csv('kaggle_val_dataset_clear_text_6000.csv')
test_df.to_csv('kaggle_test_dataset_clear_text_6000.csv')

print("train_df size=",train_df.shape)
print("val_df size=",val_df.shape)
print("test_df size=",test_df.shape)


#train_df = pd.read_csv(test_path,usecols = (['category','description']))
#train_df.dropna(inplace=True)
#train_df.sort_values(by=['category','description'],ascending=True)
#train_df.columns=['y','text']
#print(np.any(train_df.isnull())==True) 
#train_df.to_csv('spark_train_data.csv',header = ['y', 'text'])

#print(train_df.head(50))
