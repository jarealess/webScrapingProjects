import tweepy
from tweepy import OAuthHandler
import pandas as pd
import time
import json
import re
import chardet
from datetime import datetime

from yaml import serialize

#tweepy documentation:  https://docs.tweepy.org/en/stable/
#article: https://medium.com/analytics-vidhya/scraping-twitter-data-using-tweepy-8005d7b517a3

## --------------- conexión  -------------------------------------

consumer_key = '5b14HpQBIPwuQLyeBAlE3VtVf'
consumer_secret = 'Sw6BXwTcgwMB4aTrIojIaUJwupuO8aLDNmDWsABSdBrZYD7piB'
access_token = '215795033-tgmUfdhVSXoNBSzqnDTetuAP6RbjNnvq5rOpq6JM'
access_token_secret = 'R1fis8a3r56Ut78fXO82vff0gZTP9oVFiCvvAYw4Kr1bh'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True) 

# --------------------- Get Specific tweet text  ----------------------------------------------------------------------       

def fnGetTweetText(status_id=None):
    """fnGetTweetText ---> Retorna el texto del tweet con id = status_id"""
    
    ### ------------ solicitar id
    if status_id == None:
        status_id = input('Ingrese id del tweet: ')

    ### ----- buscar tweet
    try:
        status = api.get_status(id = status_id, tweet_mode="extended")
        tText = status.retweeted_status.full_text

    except: #AttributeError:  # Not a Retweet
        tText = ''
    
    return tText



## -------------------------- Formatear fecha -------------------------------------------------------
def formatDate(string):
    """formatDate ---> Extrae el día, mes y año de la fecha que está en la forma 'Sun Mar 20 21:05:43 +0000 2022'
                       y los convierte a datetime"""

    pattern = r'[ ](\b[a-zA-Z]{3}\b)[ ](\b[0-9]{2}\b).+[ ](\b\d{4}\b)$'
    grupos = re.search(pattern, string)
    
    # capturamos los grupos
    mes, dia, anio = grupos.groups()

    # convertimos a tiempo
    result = datetime.strptime(f'{mes} {dia} {anio}', '%b %d %Y')
    return result


#------------------------------- user tweets ----------------------------------------------------------------------

def fnGetUserTimeLine(username, count):
    """fnGetUserTimeLine ---> Extrae cierta cantidad (count) de tweets para el usuario especificado (username)
                              y los organiza por fecha"""

    user_tweets = []
    try:     
        # Creation of query method using appropriate parameters
        tweets = tweepy.Cursor(api.user_timeline,user_id=username, include_rts=False).items(count)
    
        # Pulling information from tweets iterable object and adding relevant tweet information in our data frame
    
        for tweet in tweets:
            user_tweets.append(
                            {'Created at' : tweet._json['created_at'],
                                        'User ID': tweet._json['id_str'],
                                #'User Name': tweet.user._json['name'],
                                            'Text': tweet._json['text'],
                        #'Description': tweet.user._json['description'],
                         #   'Location': tweet.user._json['location'],
                'Followers Count': tweet.user._json['followers_count'],
                    'Friends Count': tweet.user._json['friends_count'],
                'Statuses Count': tweet.user._json['statuses_count']
            #'Profile Image Url': tweet.user._json['profile_image_url']
                            })
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)

    sorted_tweets = sorted(user_tweets, reverse=True, key=lambda x: formatDate(x['Created at']))
    return json.dumps(sorted_tweets, indent=2)


## ----------------------------- tweets  -----------------------------------------------------------------------------

# definición columnas:  https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets


def fnGetTopicTweets(topic, count):
    """fnGetTopicTweets ---> Retorna una cantidad de tweets (count) acerca de un tema (topic) ingresado"""

    topic_tweets = []

    ## -------------- filling in the dataframe
    try:
        # Creation of query method using appropriate parameters
        tweets = tweepy.Cursor(api.search_tweets,q=topic,result_type='recent', lang = 'es').items(count)

        # Pulling information from tweets iterable object and adding relevant tweet information in our data frame
        for tweet in tweets:
            topic_tweets.append(
                            {'Created at' : tweet._json['created_at'],
                                    'Status ID': tweet._json['id_str'],
                                        #'User ID': tweet.user._json['id'],
                                        'User': tweet.user._json['screen_name'],
                                #'User Name': tweet.user._json['name'],
                                            'Text': tweet._json['text'],
                                            #'urls': tweet._json['entities']['urls'],
                        # 'Description': tweet.user._json['description'],
                            'Location': tweet.user._json['location'],
                    'Favorites': tweet.user._json['favourites_count'],
                    'Retweets': tweet._json['retweet_count'],
                    'retweeted': tweet._json['retweeted'],
                    #'Friends Count': tweet.user._json['friends_count'],
                    #'Zone': tweet.user._json['time_zone'],
                #   'Place': tweet.user._json['place'],
                    'Verified account':  tweet.user._json['verified'],
                    #'Internal Links':  tweet.user._json['url']
                            } )
    
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)

    ### ----------- texto completo 
    for tweet in topic_tweets:
        tweet['Text'] = fnGetTweetText(tweet['Status ID'])

    ##-------------- ordenado 
    topic_tweets = sorted(topic_tweets, reverse=True, key=lambda x : formatDate(x['Created at']))

    return json.dumps(topic_tweets, indent=2, ensure_ascii=False)



#------------------------- funciones ------------------------------------------
#print(formatDate('Mon Mar 14 00:37:08 +0000 2022'))
#print(fnGetTweetText('1521844282365259783'))
#print(fnGetTopicTweets('Elon Musk', 20))
#print(fnGetUserTimeLine('janickreales', 30))
