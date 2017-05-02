import tweepy
from textblob import TextBlob

# Step 1 - Authenticate
consumer_key = 'OpOG4AEyEUPZorhowWpu3YeoB'
consumer_secret = 'za0IA6XUq57erUqAanneZBXLpGkHZXcq2lUiIoRVtdUidVJe88'

access_token = '2891442361-9odBwzwZoxgUOFzo41BSE0ZC62pDKaDThJMVDDT'
access_token_secret = 'vx5uiHTJzU11lGbKsv8BsbeS6bqy4b1pdxedMCaHWqCtw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Step 3 - Retrieve Tweets
public_tweets = api.search('Trump')

# CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
# and label each one as either 'positive' or 'negative', depending on the sentiment
# You can decide the sentiment polarity threshold yourself

for tweet in public_tweets:
    print(tweet.text)

    # Step 4 Perform Sentiment Analysis on Tweets
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print("")
