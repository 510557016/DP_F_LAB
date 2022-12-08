import os
import nltk
from PIL import Image
import pytesseract
import readability
import string
import collections
import string
from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
from GoogleNews import GoogleNews

#圖片
#img = Image.open('time.png')
#text = pytesseract.image_to_string(img, lang='eng')
#print(text)

#全域變數
global type_list , key_word
type_list = {}

#搜尋Google News 關鍵字新聞
googlenews_key_word = 'TSMC' 
#googlenews_key_word = 'FIFA2022' 
key_word = googlenews_key_word
googlenews = GoogleNews()
googlenews.clear()
googlenews.set_lang('en')
googlenews.set_period('1d')
#googlenews.set_time_range('12/04/2022','12/04/2022')
googlenews.set_encode('utf-8')
googlenews.get_news(googlenews_key_word)
googlenews.search(googlenews_key_word)
#區間內共有幾筆關鍵字新聞
googlenews_count = googlenews.total_count()
print("googlenews_count =", googlenews_count)
#顯示第2頁(每頁固定10筆)
#result = googlenews.page_at(2)
#link = googlenews.get_links()
#text = googlenews.get_texts()
result = []
num = 2
for num in range(9):
	result_page = googlenews.page_at(num)
	result.extend(result_page)
#link = googlenews.get_links()
text = googlenews.get_texts()
#第一筆新聞內容
print(len(result[0]))
print(result[0])
#標題
print(result[0]['title']) 
#連結
print(result[0]['link'])
#描述
print(result[0]['desc'].replace('\n', ''))
#正文摘要
print(text[0].replace('\n', ''))
# sum of news
rows = len(result)
#cols = len(result[0])
#total_elements = rows * cols
#print(total_elements)  
print("sum of news = ", rows)
sum_of_news = int(rows) 
#模擬分析
def model_analysis(text,num):
	type_selection = int(num) % 4

	if(text=="TSMC"):
		if(type_selection == 0):
			type_prediction = 'fab21'
		if(type_selection == 1):
			type_prediction = 'Arizona'
		if(type_selection == 2):
			type_prediction = 'Apple'
		if(type_selection == 3):
			type_prediction = 'Morris Chang'
	elif(text=="FIFA2022"):
		if(type_selection == 0):
			type_prediction = 'Quarter'
		if(type_selection == 1):
			type_prediction = 'Cristiano Ronaldo'
		if(type_selection == 2):
			type_prediction = 'prediction'
		if(type_selection == 3):
			type_prediction = 'Messi'	 
	else:
		if(type_selection == 0):
			type_prediction = 'A'
		if(type_selection == 1):
			type_prediction = 'B'
		if(type_selection == 2):
			type_prediction = 'C'
		if(type_selection == 3):
			type_prediction = 'D' 			
	
	return type_prediction

def draw_PieChart(type_list , key_word):
	print(type_list)
	list_labels = list(type_list.keys())
	values = list(type_list.values())
	total = sum(type_list.values())
	plt.title("Analyze " + key_word + " PieChart", {"fontsize" : 18})
	plt.pie(values, labels=list_labels, autopct=lambda p: '{:.0f}%'.format(p * total / 100))
	plt.legend(loc = "best")  
	plt.show()
	
print("===== nltk =====")
#移除停用符號
#print("標點符號 : ",string.punctuation)
#讀取停用詞
stopword_list = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
#詞型還原
lem = nltk.WordNetLemmatizer()
#移除停用詞
def remove_stopword(text, is_lower_case=False):
	if is_lower_case:
		text = text.lower()
	#篩選數字	
	tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')	
	#分詞	
	#tokens = nltk.word_tokenize(text)
	tokens = tokenizer.tokenize(text)
	#tokens = [tokens.strip() for tokens in tokens]
	tokens = [lem.lemmatize(tokens.strip()) for tokens in tokens]
	filtered_tokens = [tokens for tokens in tokens if tokens not in stopword_list]
	filtered_text = ' '.join(filtered_tokens)
	return filtered_text , filtered_tokens

for num in range(sum_of_news):
	print("title = ",result[num]['title'].replace('\n', ''))
	print("desc  = ",result[num]['desc'].replace('\n', ''))
	print("text  = ",text[num].replace('\n', ''))
	print("link  = ",result[num]['link'].replace('\n', ''))
	#html
	#url = result[num]['link'].replace('\n', '')
	#print("url=",url)
	#response = urllib.request.urlopen(url)
	#html = response.read()
	# 清除 html tag
	#soup = BeautifulSoup(html,"html5lib")
	#搜尋本文
	#html_text = soup.get_text(strip=True)
	
	filtered_text,filtered_tokens = remove_stopword(result[num]['title']+result[num]['desc']+text[num],True)
	#print(filtered_text)

	#生字表集合
	word_freqs = collections.Counter()
	for word in filtered_tokens:
		word_freqs[word]+=1
	#print(word_freqs.most_common(20))
	#轉換爲字典後輸出
	for word,count in enumerate(dict(word_freqs.most_common(20)).items()):
	    print(count)	

	#title/desc/text/filtered_text/ 傳送至 訓練好的 model 判斷分類 (ToDo...)  
	print("===== model_prediction =====")
	type_prediction = model_analysis(key_word,num)
	print("===== type in dict =====")
	if type_prediction not in type_list.keys():
		type_list[type_prediction] = 1
	else:
		count = type_list.get(type_prediction)
		total_count = count + 1	
		# dict = {string : int}
		up_dict = {type_prediction:total_count} 
		type_list.update(up_dict)
		
	#內文評分    
	#results = readability.getmeasures(text, lang='en')
	#print("readability grades")
	#print("LIX grades: ",results['readability grades']['LIX'])
	#print("Coleman-Liau grades: ",results['readability grades']['Coleman-Liau'])    

#畫出分類圓餅圖
draw_PieChart(type_list,key_word)
