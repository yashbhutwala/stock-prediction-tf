import os
import sys
import requests
import numpy as np
import tweepy

from textblob import TextBlob
from keras.models import Sequential
from keras.layers import Dense

# Step 1 - Authenticate
consumerKey = 'OpOG4AEyEUPZorhowWpu3YeoB'
consumerSecret = 'za0IA6XUq57erUqAanneZBXLpGkHZXcq2lUiIoRVtdUidVJe88'

accessToken = '2891442361-9odBwzwZoxgUOFzo41BSE0ZC62pDKaDThJMVDDT'
accessTokenSecret = 'vx5uiHTJzU11lGbKsv8BsbeS6bqy4b1pdxedMCaHWqCtw'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

user = tweepy.API(auth)


def stockSentiment(stockName, numTweets=100):
    """Checks if the sentiment for our stockName is positive or negative,
    returns True if majority of valid tweets have positive sentiment"""

    listOfTweets = user.search(stockName, count=numTweets)
    threshold = posSentTweet = negSentTweet = 0

    for tweet in listOfTweets:
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity >= threshold:
            posSentTweet = posSentTweet + 1
        else:
            negSentTweet = negSentTweet + 1

    if posSentTweet > negSentTweet:
        print("Overall Positive")
        return True
    else:
        print("Overall Negative")
        return False


def getHistoricalData(stockName):
    # Download our file from google finance
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A' + stockName + '&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(FILE_NAME, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return True

    return False


def stockPrediction(FILE_NAME):
    # Collect data points from csv
    dataset = []

    with open(FILE_NAME) as f:
        for n, line in enumerate(f):
            if n != 0:
                dataset.append(float(line.split(',')[4]))

    dataset = np.array(dataset)

    # Create dataset matrix (X=t and Y=t+1)
    def createDataset(dataset):
        dataX = [dataset[n + 1] for n in range(len(dataset) - 2)]
        return np.array(dataX), dataset[2:]

    trainX, trainY = createDataset(dataset)

    # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, nb_epoch=200, batch_size=2, verbose=2)

    # Our prediction for tomorrow
    prediction = model.predict(np.array([dataset[0]]))
    result = 'The price will move from %.2f to %.2f' % (
        dataset[0], prediction[0][0])
    return result


if __name__ == "__main__":
    # Where the csv file will live
    FILE_NAME = 'historicalData.csv'
    # Ask user for a stock name
    stockName = input(
        'Enter a stock quote from NASDAQ (i.e: AAPL, FB, GOOGL): ').upper()

    if not stockSentiment(stockName):
        print('This stock has bad sentiment, please re-run the script')
        sys.exit()

    # Check if we have the historical data for the stockName
    if not getHistoricalData(stockName):
        print('Google returned a 404, please re-run the script and enter a valid stock quote from NASDAQ')
        sys.exit()

    # We have our file so we create the neural net and get the prediction
    print(stockPrediction(FILE_NAME))

    # We are done so we delete the csv file
    os.remove(FILE_NAME)
