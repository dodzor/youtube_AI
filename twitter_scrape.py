import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()
limit= 100 
tweets_list =[] 
for tweet in sntwitter.TwitterSearchScraper("Keto diet Cookbook Amazon").get_items(): 
    if len(tweets_list)== limit: 
        break 
    else: 
        tweets_list.append([tweet.date, tweet.rawContent, tweet.retweetCount, tweet.likeCount])
        # sentiment = analyzer.polarity_scores(tweet.content)
        # print(tweet.content)
        # print(sentiment)
        # print("-------------------------------------------------")

df = pd.DataFrame(tweets_list,columns=["date", "tweets", "retweetcounts", "likecounts"])   
# print(df)
# print("-------------------------------------------------")

# q: function to list tweets in decending order of sentiment score

def sort_by_sentiment(df):
    df['sentiment_score'] = df['tweets'].apply(lambda x: analyzer.polarity_scores(x))
    df['sentiment_score'] = df['sentiment_score'].apply(lambda x: x['compound'])
    df['link'] = df['tweets'].str.extract(r'(https?://t\.co/\w+)')
    df = df.sort_values(by='sentiment_score', ascending=False)
    df = df.head(10)[['tweets', 'sentiment_score', 'link']]
    print(df)
    return df

df = sort_by_sentiment(df)

# book_title = df.loc[0,"tweets"]
# sentiment = analyzer.polarity_scores(book_title)
# sentiment = df.loc[0, "sentiment_score"]
# print(book_title)
# print(sentiment)


# import openai

# openai.api_key = ""

# # "Summarize the item.description in two sentences".
# prompt = "Summarize this in two sentences: " + book_title

# book_summary = openai.Completion.create(
#   model = "text-davinci-003",
#   prompt = prompt,
#   temperature = 1,
#   max_tokens = 600,
#   top_p = 1,
#   frequency_penalty = 0,
#   presence_penalty = 0
# )

# print(book_summary)


# book_title = df.loc[0,"tweets"]
# sentiment = analyzer.polarity_scores(book_title)
# print(book_title)
# print(sentiment)