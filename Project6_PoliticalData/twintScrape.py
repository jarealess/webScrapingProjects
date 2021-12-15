#Twint utilizes Twitter's search operators to let you scrape Tweets from specific users, scrape Tweets relating to certain topics, 
# hashtags & trends, or sort out sensitive information from Tweets like e-mail and phone numbers. I find this very useful, 
# and you can get really creative with it too.

#Twint also makes special queries to Twitter allowing you to also scrape a Twitter user's followers, Tweets a user has liked, 
# and who they follow without any authentication, API, Selenium, or browser emulation.

#taken from:  https://github.com/twintproject/twint



import twint

##-------------- get user tweets information  > PANDAS --------------
def twintGetTweetsDf(SearchList):
    c = twint.Config()
    #c.Username=Username
    c.Search = SearchList      # topic
    c.Limit = 500     # number of Tweets to scrape
    c.Pandas = True       # store tweets in a csv file
    c.Min_likes = 0
    c.Hide_output = True
    # c.Since = '2021-12-01'
    #c.Until = '2021-12-05'

    twint.run.Search(c) 
    Tweets_df = twint.storage.panda.Tweets_df
    print(Tweets_df[['date', 'name', 'tweet', 'retweet']])


##-------------- get user tweets information > CSV --------------
def twintGetTweetsCsv(Username,filename, SearchList):
    c = twint.Config()
    c.Username= Username  #'POTUS'
    c.Search =  SearchList #['us'] # topic
    c.Limit = 500      # number of Tweets to scrape
    c.Store_csv = True       # store tweets in a csv file
    c.Output = filename+".csv"     # path to csv file

    twint.run.Search(c) 


##-------------- get user profile information --------------
def twintGetProfileInfo(Username):
    c = twint.Config()
    c.Username=Username
    twint.run.Lookup(c)


#twintGetTweetsDf(['duque', 'colombia'])
#twintGetProfileInfo('POTUS')