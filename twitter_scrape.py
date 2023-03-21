import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()
limit= 10 
tweets_list =[] 
for tweet in sntwitter.TwitterSearchScraper("Keto diet book Amazon").get_items(): 
    if len(tweets_list)== limit: 
        break 
    else: 
        tweets_list.append([tweet.date, tweet.content, tweet.user.username, tweet.user.displayname, tweet.user.description,  
        tweet.replyCount, tweet.retweetCount,tweet.likeCount , tweet.quoteCount, tweet.lang, tweet.source]) 
df = pd.DataFrame(tweets_list,columns=["date", "tweets", "username", "displayname", "description", "rpcounts", 
                                        "retweetcounts", "likecounts", "quotecount", "languvage", "source"  ])   
print(df)

book_title = df.loc[0,"tweets"]
sentiment = analyzer.polarity_scores(book_title)
print(book_title)
print(sentiment)