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
from GoogleNews import GoogleNews

#圖片
#img = Image.open('time.png')
#text = pytesseract.image_to_string(img, lang='eng')
#print(text)

#搜尋Google News 關鍵字新聞
googlenews_key_word = 'FIFA2022'
googlenews = GoogleNews()
googlenews.clear()
googlenews.set_lang('en')
googlenews.set_period('1d')
#googlenews.set_time_range('12/04/2022','12/04/2022')
googlenews.set_encode('utf-8')
googlenews.get_news(googlenews_key_word)
googlenews.search(googlenews_key_word)
result = googlenews.page_at(2)
#link = googlenews.get_links()
text = googlenews.get_texts()
print(len(result[0]))
print(result[0])
#標題
print(result[0]['title']) 
#連結
print(result[0]['link'])
#描述
print(result[0]['desc'].replace('\n', ''))
#正文
print(text[0].replace('\n', ''))
# sum of news
rows = len(result)
#cols = len(result[0])
#total_elements = rows * cols
#print(total_elements)  
print("sum of news = ", rows)
sum_of_news = int(rows) 

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
	#send(title,desc,link,text,filtered_text)  

	#內文評分    
	#results = readability.getmeasures(text, lang='en')
	#print("readability grades")
	#print("LIX grades: ",results['readability grades']['LIX'])
	#print("Coleman-Liau grades: ",results['readability grades']['Coleman-Liau'])    


