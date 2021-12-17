import tweepy
from tweepy import OAuthHandler
import pandas as pd
import time


#tweepy documentation:  https://docs.tweepy.org/en/stable/
#article: https://medium.com/analytics-vidhya/scraping-twitter-data-using-tweepy-8005d7b517a3

## --------------- conexión  -------------------------------------

consumer_key = 'xxxx'
consumer_secret = 'xxxxx'
access_token = 'xxxxx'
access_token_secret = 'xxxxxxx'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True) 



#------------------------------- user tweets ----------------------------------------------------------------------

def fnGetUserTimeLine(username, count):

    df_user_tweets = pd.DataFrame()
    try:     
        # Creation of query method using appropriate parameters
        tweets = tweepy.Cursor(api.user_timeline,user_id=username).items(count)
    
        # Pulling information from tweets iterable object and adding relevant tweet information in our data frame
    
        for tweet in tweets:
            df_user_tweets = df_user_tweets.append(
                            {'Created at' : tweet._json['created_at'],
                                       # 'User ID': tweet._json['id'],
                                #'User Name': tweet.user._json['name'],
                                            'Text': tweet._json['text'],
                        #'Description': tweet.user._json['description'],
                         #   'Location': tweet.user._json['location'],
                'Followers Count': tweet.user._json['followers_count'],
                    'Friends Count': tweet.user._json['friends_count'],
                'Statuses Count': tweet.user._json['statuses_count']
            #'Profile Image Url': tweet.user._json['profile_image_url']
                            }, ignore_index=True)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)

    print(df_user_tweets.head())

    return df_user_tweets



# --------------------- Get Specific tweet text  ----------------------------------------------------------------------       

def fnGetTweetText(status_id):
    
    try:
        status = api.get_status(id = status_id, tweet_mode="extended")
        tText = status.retweeted_status.full_text
    except: #AttributeError:  # Not a Retweet
        tText = ''
    
    return tText



## ----------------------------- tweets  -----------------------------------------------------------------------------

# definición columnas:  https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets


def fnGetTweets(topic, count):
    df_query_based_tweets = pd.DataFrame()


    ## -------------- filling in the dataframe
    try:
        # Creation of query method using appropriate parameters
        tweets = tweepy.Cursor(api.search_tweets,q=topic).items(count)

        # Pulling information from tweets iterable object and adding relevant tweet information in our data frame
        for tweet in tweets:
            df_query_based_tweets = df_query_based_tweets.append(
                            {'Created at' : tweet._json['created_at'],
                                    'Status ID': tweet._json['id_str'],
                                        'User ID': tweet.user._json['id'],
                                        'User': tweet.user._json['screen_name'],
                                'User Name': tweet.user._json['name'],
                                            'Text': tweet._json['text'],
                                            'urls': tweet._json['entities']['urls'],
                        # 'Description': tweet.user._json['description'],
                            'Location': tweet.user._json['location'],
                    'Favorites': tweet.user._json['favourites_count'],
                    'Friends Count': tweet.user._json['friends_count'],
                    'Zone': tweet.user._json['time_zone'],
                #   'Place': tweet.user._json['place'],
                    'Verified account':  tweet.user._json['verified'],
                    'Internal Links':  tweet.user._json['url']
                            }, ignore_index=True)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)



    ## search_tweets doesn't bring the full tweet, so I use the function fnGetTweetText to do it
    df_query_based_tweets['Text'] = df_query_based_tweets['Status ID'].apply(lambda x: fnGetTweetText(x))

    ##-------------- save it to csv
    df_query_based_tweets.to_csv('tweetsOutput.csv', index=False, encoding='utf-8', sep=';')
    print(df_query_based_tweets.head())

    return df_query_based_tweets




# print(fnGetTweetText('1471570132aaa4031488'))
fnGetTweets('Ivan Duque', 150)
# fnGetUserTimeLine('twitter', 150)