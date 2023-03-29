import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import openai
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

analyzer = SentimentIntensityAnalyzer()
limit= 10 
tweets_list =[] 
for tweet in sntwitter.TwitterSearchScraper("Chinese history book Amazon").get_items(): 
    if len(tweets_list)== limit: 
        break 
    else: 
        tweets_list.append([tweet.date, tweet.rawContent, tweet.retweetCount, tweet.likeCount])

df = pd.DataFrame(tweets_list,columns=["date", "tweets", "retweetcounts", "likecounts"])   

# sort tweets in decending order of sentiment score
def sort_by_sentiment(df):
    df['sentiment_score'] = df['tweets'].apply(lambda x: analyzer.polarity_scores(x))
    df['sentiment_score'] = df['sentiment_score'].apply(lambda x: x['compound'])
    df['link'] = df['tweets'].str.extract(r'(https?://t\.co/\w+)')
    df = df.sort_values(by='sentiment_score', ascending=False)
    df = df.head(10)[['tweets', 'sentiment_score', 'link']]

    # Reset the index of the DataFrame
    df.reset_index(drop=True, inplace=True)

    # Get the title of the first tweet
    first_tweet_title = df.iloc[0]['tweets']

    return df, first_tweet_title

sorted_df, first_tweet_title = sort_by_sentiment(df)

# create book summary based on tweet title
openai.api_key = os.environ['OPENAI-API-KEY']
prompt = "Summarize this in two sentences: " + first_tweet_title

book_summary = openai.Completion.create(
  model = "text-davinci-003",
  prompt = prompt,
  temperature = 1,
  max_tokens = 600,
  top_p = 1,
  frequency_penalty = 0,
  presence_penalty = 0
)

# generate video from book summary and image
url = "https://api.d-id.com/talks"
script = book_summary['choices'][0]['text']
print(script)

payload = {
    "script": {
        "type": "text",
        "provider": {
            "type": "microsoft",
            "voice_id": "Jenny"
        },
        "ssml": "false",
        "input": script
    },
    "config": {
        "fluent": "false",
        "pad_audio": "0.0"
    },
    "source_url": "https://i.postimg.cc/Jn6KqzcF/07ada757-70e8-4282-86d7-aa7b3b09fdf9.jpg"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer " + os.environ['D-ID-BEARER']
}

response = requests.post(url, json=payload, headers=headers)
# print(response.text)

#wait for 20 seconds for the video to be generated
time.sleep(20)

id = response.json()['id']
# id = "tlk_R-cPzrkz3jXgRJyqq_PjD"
response = requests.get(url + '/' + id, headers=headers)
print(response.json())
