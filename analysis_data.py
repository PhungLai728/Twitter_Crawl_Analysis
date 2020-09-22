import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

############# Data analysis #############
# Read data
all_info = pd.read_csv('covid19.csv')
tweet_content = all_info['tweet content']
year_posted = all_info['year']
month_posted = all_info['month']
day_posted = all_info['day']
hour_posted = all_info['hour']
tweet_source = all_info['source']
tweet_friends = all_info['friends']

# Check the unique of the data 
tweet_content_u = tweet_content.unique().tolist()
year_posted_u = year_posted.unique().tolist()
month_posted_u = month_posted.unique().tolist()
day_posted_u = day_posted.unique().tolist()
hour_posted_u = hour_posted.unique().tolist()
tweet_source_u = tweet_source.unique().tolist()
tweet_friends_u = tweet_friends.unique().tolist()

# Number of tweets in 2019 and 2020
occurrences = lambda s, lst: (i for i,e in enumerate(lst) if e == s)
year2019 = len(list(occurrences(2019,year_posted))) # 786
year2020 = len(list(occurrences(2020,year_posted))) # 1367

# Histogram of monthly usage
plt.hist(month_posted, bins=12, edgecolor='white', linewidth=1.2)
plt.ylabel('Number of tweets')
plt.xlabel('Month')
plt.show()

# Histogram of daily usage
plt.hist(day_posted, bins=31, edgecolor='white', linewidth=1.2)
plt.ylabel('Number of tweets')
plt.xlabel('Day')
plt.show()

# Histogram of hourly usage
plt.hist(hour_posted, bins=24, edgecolor='white', linewidth=1.2)
plt.ylabel('Number of tweets')
plt.xlabel('Hour')
plt.show()



############# Tweet content analysis #############
def remove_content(text):
    text = re.sub(r"http\S+", "", text) #remove urls
    text=re.sub(r'\S+\.com\S+','',text) #remove urls
    text=re.sub(r'\@\w+','',text) #remove mentions
    text =re.sub(r'\#\w+','',text) #remove hashtags
    return text

def process_text(text, stop_words, stem=False): #clean text
    text=remove_content(text)
    text = re.sub('[^A-Za-z]', ' ', text.lower()) #remove non-alphabets
    tokenized_text = word_tokenize(text) #tokenize
    clean_text = [
         word for word in tokenized_text
         if word not in stop_words]
    if stem:
        clean_text=[stemmer.stem(word) for word in clean_text]
    return ' '.join(clean_text)

stopw = stopwords.words('english')
tmp_tweets = tweet_content.apply(lambda x: process_text(x,stopw))

filter_list = ['b','x','xa', 'rt', 'xe', 'xc', 'https','xb','xf','xbb','xef','de','xd','xac','ed','xce','xcf']
cleaned_tweets = []
for i in range(len(tmp_tweets)):
    tmp = tmp_tweets[i].split()
    tmp2 = [j for j in tmp if j not in filter_list]
    tmp2 = ' '.join(tmp2)
    cleaned_tweets.append(tmp2)

from wordcloud import WordCloud, STOPWORDS
temp = ' '.join(cleaned_tweets)
wordcloud = WordCloud(width = 800, height = 500, 
                background_color ='white', 
                min_font_size = 10).generate(temp)
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0) 
plt.show()

from sklearn.feature_extraction.text import CountVectorizer
def plot_ngram(sentences, ngram_range=(1,3), top=20,firstword=''):
    c=CountVectorizer(ngram_range=ngram_range)
    X=c.fit_transform(sentences)
    words=pd.DataFrame(X.sum(axis=0),columns=c.get_feature_names()).T.sort_values(0,ascending=False).reset_index()
    res=words[words['index'].apply(lambda x: firstword in x)].head(top)
    t1 = [i for i in res['index'] ]
    t2 = [i for i in res[0] ]
    plt.bar(t1,t2)
    plt.xticks(rotation=45)
    plt.ylabel('count')
    plt.show()

plot_ngram(cleaned_tweets, ngram_range=(1,1))
plot_ngram(cleaned_tweets, ngram_range=(2,2))

from textblob import TextBlob
sentiment = tweet_content.apply(lambda x:TextBlob(x).sentiment[0])
polarity = sentiment.apply(lambda x: 'pos' if x>=0 else 'neg')

fig, ax = plt.subplots()
N, bins, patches = ax.hist(polarity, bins=2, edgecolor='white', linewidth=1)
patches[0].set_facecolor('b')
patches[1].set_facecolor('r')
plt.ylabel('count')
plt.xlabel('polarity')
plt.show()

print('Well Done!')