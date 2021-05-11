import csv
import pandas as pd
from textblob import TextBlob
from PIL import Image
from wordcloud import STOPWORDS, WordCloud
import numpy as np


##TOKENIZATION
print("TOKENIZATION\n")
input_csv = pd.read_csv('DM_Raw_Data_.csv', encoding='ISO-8859-1')


#Parse csv's to only extract column called 'message'
messages1 = list(input_csv['MsgBody'])
#messages= messages.astype(str)
messages='.'.join(str(e) for e in messages1)
#print (messages)

text_blob_object = TextBlob(messages)
document_sentence=text_blob_object.sentences
document_words=text_blob_object.words

#Print tokenized sentences
print(document_sentence)
print("\n")
#Print number of sentences
print("No. of sentences:", len(document_sentence))
print("\n")

#Print words
#print(document_words)
print("\n")
# #Print number of words
print("No. of words:",len(document_words))
print("\n")

#find stock tickers from the input data

import re #for regex on scraped text
regex = re.compile('[^a-zA-Z ]')
word_dict = {}

for x in document_words:
        
        if x in ['A', 'B', 'GO', 'ARE', 'ON', 'IT', 'ALL', 'NEXT', 'PUMP', 'AT', 'NOW', 'FOR', 'TD', 'CEO', 'AM', 'K', 'BIG', 'BY', 'LOVE', 'CAN', 'BE', 'SO', 'OUT', 'STAY', 'OR', 'NEW','RH','EDIT','ONE','ANY']:
            pass
        elif x in word_dict:
            word_dict[x] += 1
        else:
            word_dict[x] = 1

word_df = pd.DataFrame.from_dict(list(word_dict.items())).rename(columns = {0:"Term", 1:"Frequency"})

print(word_df)


ticker_df = pd.read_csv('tickers.csv').rename(columns = {"Symbol":"Term", "Name":"Company_Name"})
stocks_df = pd.merge(ticker_df, word_df, on="Term")


stocks_df = stocks_df.sort_values(by="Frequency", ascending = False, ignore_index = True).head(20)

stocks_df.to_csv(r'stocks_output.csv')

#find the sentences that has the above stocks

listofstocks=stocks_df["Term"]
mentions=[]
listt=[]

for i in document_sentence:
    for j in listofstocks:
        if j in i:
            mentions.append(i)
            listt.append(j)
print(mentions)
print(listt)

df_mentions = pd.DataFrame()

df_mentions['mentions']=pd.Series(mentions)
df_mentions['ticker']=pd.Series(listt)
#df_mentions.to_csv(r'mentions.csv')

print(df_mentions)
b1=pd.Series(mentions)
print (b1)
# sentiment polarities for the sentences
df1=pd.DataFrame()

b=[]
for j in mentions:
    b.append(TextBlob(str(j)).sentiment.polarity)

print(b)
df1["polarity"]=b
df1["Sentence"]=mentions
print(df1)
df1.to_csv('mentions_polarity.csv')




#wordcloud

wci = pd.read_csv('file with emojis.csv', encoding='ISO-8859-1')


#Parse csv's to only extract column called 'message'
d1 = list(wci['Column6'])


d1= ["love", "fuck", "hedge","time", "buying","stock","just", "shares","gme","im"]

d2=["moon","holding","apes","diamond","hands","stock","hold","like","gme","amc"]

d='.'.join(str(e) for e in d2)

# Read the whole text
text = d

wc = WordCloud(
    background_color="white",max_words=100,).generate(text)

# Display the generated wordcloud image using pillow
image = wc.to_image()
image.show()


