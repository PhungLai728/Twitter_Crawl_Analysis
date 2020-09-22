import tweepy
import pandas as pd

consumer_key = 'change with your consumer key'
consumer_secret = 'change with your consumer secret'
access_token = 'change with your access token'
access_secret = 'change with your access secret'

tweetsPerQry = 100
maxTweets = 10000
hashtag = "#covid"


authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
maxId = -1
tweetCount = 0

result_path = 'covid19'
num = 0
iteration = []
tweets_collected = []
id_info = []
time_posted_year = []
time_posted_month = []
time_posted_day = []
time_posted_hour = []
tweet_source = []
tweet_friends = []
tweet_geo = []

while tweetCount < maxTweets:
    if(maxId <= 0):
        newTweets = api.search(q=hashtag, count=tweetsPerQry, result_type="recent", tweet_mode="extended")
    else:
        newTweets = api.search(q=hashtag, count=tweetsPerQry, max_id=str(maxId - 1), result_type="recent", tweet_mode="extended")

    if not newTweets:
        print("Tweet Habis")
        break
	
    for tweet in newTweets:
        print('------')
        print('num',num)
        iteration.append(num)
        num += 1

        print(tweet.full_text.encode('utf-8'))
        tweets_collected.append(tweet.full_text.encode('utf-8'))
        id_info.append(tweet.id)
        time_posted_year.append(tweet.user.created_at.year)
        time_posted_month.append(tweet.user.created_at.month)
        time_posted_day.append(tweet.user.created_at.day)
        time_posted_hour.append(tweet.user.created_at.hour)

        tweet_source.append(tweet.source)
        tweet_friends.append(tweet.user.friends_count)
        tweet_geo.append(tweet.geo)

        print('saving to excel')
        data_w = {'tweet count': iteration, 'id':id_info, 'tweet content': tweets_collected,
        'year':time_posted_year, 'month':time_posted_month,'day':time_posted_day,'hour':time_posted_hour,
        'source':tweet_source, 'friends':tweet_friends, 'geo':tweet_geo}  
        my_csv = pd.DataFrame(data_w)
        name_save = result_path + '.csv' 
        my_csv.to_csv( name_save, index=False)
    
    tweetCount += len(newTweets)	
    maxId = newTweets[-1].id

# consumer_key = 'Fl06AlnGGGnj3gO9aEptI0yoW'
# consumer_secret = 'fciFbasgcNmIq6RJLoeyxj6YX6zrWDPSHa7JJYnnwWLO9rpuxa'
# access_token = '1308129394511302658-LidgfrveZFsArxjj1saL7UdmlyY3ZU'
# access_secret = 'udt0DIkaAure0U8DKniR6Lo90sjkYxT5f0CVGtqo6tjBM'
