import pandas as pd
import math
import requests
import string
import csv
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count




def syllable_count2(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("ed" or "es"):
        count -= 1
    if count == 0:
        count += 1
    return count



def removepunc(text,excludes):
  for char in excludes:
    text = text.replace(char,'')
  return text




def text_analysis(url,url_id):
  ans = []
  page = requests.get(url,headers={
                "Access-Control-Request-Method": "GET",
                "Origin": "*",
                "Access-Control-Request-Headers": "Authorization","user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            })
  soup = BeautifulSoup(page.content,'html.parser')
  heading = soup.find_all('h1')[0].text
  file = open(url_id+'.txt','a')  #filename
  file.write(heading.lower() +'\n')
  for i in soup.find_all('p'):
    text = i.text.strip()  #lower karna hai abhi
    file.write(text)
  file = open('StopWords_Auditor.txt','r')
  stop_aud = file.read().lower().split()
  file = open('StopWords_Currencies.txt','r',encoding='latin-1')
  stop_curr = file.read().lower().split()
  file = open('StopWords_Generic.txt','r',encoding='latin-1')
  stop_Generic = file.read().lower().split()
  file = open('StopWords_GenericLong.txt','r',encoding='latin-1')
  stop_GenL = file.read().lower().split()
  file = open('StopWords_Geographic.txt','r',encoding='latin-1')
  stop_Geo = file.read().lower().split()
  file = open('StopWords_DatesandNumbers.txt','r',encoding='latin-1')
  stop_date = file.read().lower().split()
  file = open('StopWords_Names.txt','r',encoding='latin-1')
  stop_names = file.read().lower().split()
  stop_words = stop_aud + stop_Generic + stop_GenL + stop_Geo + stop_names + stop_date + stop_curr
  file1 = open(url_id+'.txt')   
  line = file1.read()
  line = line.lower()
  words = line.split()
  for r in words:
    if not r in stop_words:
      appendFile = open(url_id+'filteredtext.txt','a')  
      appendFile.write(" "+r) 
      appendFile.close()
  file2 = open(url_id+'filteredtext.txt')   
  line = file2.read()
  words = line.split()
  word_tokens = word_tokenize(line)
  file = open('negative-words.txt', 'r',encoding='latin-1')
  neg_words = file.read().split()
  file = open('positive-words.txt', 'r',encoding='latin-1')
  pos_words = file.read().split()
  pos=0
  for r in word_tokens:
    if r in pos_words:
      pos +=1
  ans.append(pos)
  neg=0
  for r in word_tokens:
    if r in neg_words:
      neg += 1
  ans.append(neg)
  Polarity = (pos-neg)/((pos + neg) + 0.000001)
  ans.append(Polarity)
  Subjectivity = (pos+neg)/ ((len(word_tokens)) + 0.000001)
  ans.append(Subjectivity)
  sent = sent_tokenize(line)
  Average_Sentence_Length = len(words)/len(sent)
  ans.append(Average_Sentence_Length)
  complex_words=0
  for i in (words):
    if syllable_count(i) >2:
      complex_words +=1
  percentage_of_complex = complex_words/len(words)
  ans.append(percentage_of_complex)
  fog_index = 0.4*(Average_Sentence_Length + percentage_of_complex)
  ans.append(fog_index)

  file1 = open(url_id+'.txt')   #filename
  line = file1.read()
  line = line.lower()
  words = line.split()
  Average_Number_of_Words_Per_Sentence = len(words)/len(sent)
  ans.append(Average_Number_of_Words_Per_Sentence)


  ans.append(complex_words)
  
  
  stop_words = set(stopwords.words('english'))
  file2 = open(url_id+'filteredtext.txt')
  line2 = file2.read()
  words2 = line2.split()
  for r in words2:
    if not r in stop_words:
      appendFile = open(url_id+'filteredtext2.txt','a')
      appendFile.write(" "+r)
      appendFile.close()
  file3=open(url_id+'filteredtext2.txt')
  line3 = file3.read()
  words3 = line3.split()
  excludes = string.punctuation
  words4 = removepunc(line3, excludes).split()
  ans.append(len(words4))
  Syllable_Count_Per_Word=0
  for i in (words4):
    if syllable_count2(i) >0:
      Syllable_Count_Per_Word +=1
  ans.append(Syllable_Count_Per_Word)
  file = open(url_id+'.txt')
  line5 = file.read()
  words5 = line5.split()
  personal_pronoun = 0
  pronoun = ["I","you","us","we","ours","You","We","Ours"]
  for i in words5:
    if i in pronoun:
      personal_pronoun +=1
  ans.append(personal_pronoun)
  sum=0
  for i in words5:
    sum += len(i)
  Average_Word_Length = sum/len(words5)
  ans.append(Average_Word_Length)
  return ans



df = pd.read_csv('input_new.csv')
f = open('output.csv','w')
writer = csv.writer(f)
for i in range(len(df['URL'])):
  print(df['URL_ID'][i])
  try:
    answer = text_analysis(str(df['URL'][i]),str(df['URL_ID'][i]))
    l = [df['URL_ID'][i],df['URL'][i]]
    l.extend(answer)
    writer.writerow(l)
    print(l)
  except:
    pass


