# -*- coding: utf-8 -*-
"""Stock_Sentiment_Analysis (3).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TDK_Bh46fTFvgAhRs5l5AQVyU0uhVmpT

In this project we will perform sentiment analysis on three international stocks
1.NVDA
2.TSLA
3.AMZN

In this notebook I am running my command for only one stock

1. DATA COLLECTION
"""

# importing required libraries
#I scrapped data from money insider
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

# Function to scrape news articles from a given URL
def scrape_articles(url):
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html.parser')

    # Look for the correct element that contains the news articles
    news_table = html.find_all('div', class_='latest-news__story')

    articles = []
    for article in news_table:
        # Extract the title of the news article
        title = article.find('a', class_='news-link').text.strip()

        # Extract the source of the news article
        source = article.find('span', class_='latest-news__source').text.strip()

        # Extract the date of the news article
        date_tag = article.find('time', class_='latest-news__date')
        date = date_tag['datetime'] if date_tag and 'datetime' in date_tag.attrs else 'N/A'

        articles.append({
            'date_time': date,
            'source': source,
            'title': title
        })
    return articles

# List of articles
all_articles = []

# Number of pages to scrape
num_pages = 100

for page in range(1, num_pages + 1):
    url = f"https://markets.businessinsider.com/news/nvda-stock?p={page}"
    #url = f"AMZN"
    #url = f"TSLA"
    articles = scrape_articles(url)
    all_articles.extend(articles)


# Create a DataFrame from the list of articles
df = pd.DataFrame(all_articles)

# Save the DataFrame to a CSV file
csv_file = 'nvda_news_articles.csv'
df.to_csv(csv_file, index=False)
print(f"Saved {len(df)} articles to {csv_file}")

# Display the first few rows of the DataFrame

#NVDA
import pandas as pd
df = pd.read_csv( 'nvda_news_articles.csv')
df.head()

print(df.shape)

print("NVDA",df.isnull().sum())

"""PRE-PROCESSING OF DATA"""

#importing required libraries
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
import spacy
import nltk
import string
import re
nlp = spacy.load("en_core_web_lg")

"""#1.data cleaning(using regex)
#2.Tokenization and lemmatization
#3. Removing StopWords and etc.
"""

#1.Cleaning text using regex by creating a function :- clean_news_headline
import re

def clean_news_headline(headline):
    # Convert to lowercase
    headline = headline.lower()
    # Remove URLs
    headline = re.sub(r'http\S+|www\S+|https\S+', '', headline, flags=re.MULTILINE)
     # Remove special characters and punctuation (keeping only alphabets and whitespace)
    headline = re.sub(r'[^a-zA-Z\s]', '', headline)
     # Remove numbers
    headline = re.sub(r'\d+', '', headline)
     # Remove extra whitespace
    headline = re.sub(r'\s+', ' ', headline).strip()

    return headline



#Function for Removing stopwords and Punctuations :- Preprocess
nlp = spacy.load("en_core_web_lg")
preprocessed_text = []
def preprocess(text):
    doc = nlp(text)
    preprocessed_text = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        preprocessed_text.append(token.lemma_)
    return " ".join(preprocessed_text)

#Function for tokenization and stemming :- preprocess_stem
import nltk
from nltk.tokenize import word_tokenize

# downloading NLTK package
nltk.download('punkt')
# Function to preprocess and stem text
def preprocess_stem(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Perform stemming (assuming you have a stemmer defined)
    # For example, using PorterStemmer
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)



#Now applying all functions to our dataset on a new column - "preprocessed_news"
df["preprocessed_news"] = df["title"].apply(clean_news_headline)

df["preprocessed_news"] = df["preprocessed_news"].apply(preprocess)

df["preprocessed_news"] = df["preprocessed_news"].apply(preprocess_stem)

#printing first 5 files
df.head()



"""NOW WE WILL DO SOME SENTIMENT CHECK ON THE PRE-PROCESSED DATA"""

#4.Doing sentiment analysis by checking sentiment scores using Vader Sentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function to print sentiments of the sentence
def sentiment_scores(sentence):

    SIA = SentimentIntensityAnalyzer()

    # This contains pos, neg, neu, and compound scores
    sentiment_dict = SIA.polarity_scores(sentence)

    '''Below code will give how much positive,negative or neutral score does the sentence
    contains but for analysing the whole table we just need the overall sentiment score,
    thats why I am commenting out this code and printing only compound score.'''
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print( sentiment_dict['neg'],  "Negative")
    # print( sentiment_dict['neu'],  "Neutral")
    # print( sentiment_dict['pos'],  "Positive")


    return sentiment_dict['compound']

# Function to print sentiments of the sentence
def sentiment_polarity(sentence):
    SIA = SentimentIntensityAnalyzer()

    sentiment_dict = SIA.polarity_scores(sentence)

    # Decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        return "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

#Also tring to predict expected market move using sentiment
def prediction(sentiment):
    results = []

    if sentiment == "Positive":
        results.append("Price hike")
    elif sentiment == "Negative":
        results.append("Price drop")
    else:
        results.append("No price change")
    return results

#print( f"{predicted_results}")

df["sentiment"] = df["preprocessed_news"].apply(sentiment_polarity)

df["sentiment_score"] = df["preprocessed_news"].apply(sentiment_scores)

df["expected_move"] = df["sentiment"].apply(prediction)

#now defining sentiment with values "neutral" = 0,"positive"=1,"negative" =-1
#Add the new column which gives a unique number to each of these labels
df['sentiment_label'] = df['sentiment'].map({
    'Neutral' : 0,
    'Positive': 1,
    'Negative': -1,
})

df['prediction'] = df['sentiment'].map({
    'Neutral' : "No Change",
    'Positive': "Price Hike",
    'Negative': "Price Drop",
})

#printing first 5 files to check our results till now
df.head(10)

df.shape

#

"""Now comes MODEL TRAINING"""

#I used TF-IDF VECTORIZER
from sklearn.feature_extraction.text import TfidfVectorizer
TF_IDF = TfidfVectorizer(max_features=1000)

#I prefdered SupportVectorMachine as my classifier
from sklearn.svm import SVC
SVM = SVC(kernel='linear', random_state=42)

#For better performance i created a Pipeline "tfidf -->svm"
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
clf = Pipeline([
    ('tfidf', TF_IDF),
    ('svm', SVM)
])

# Split the data, preprocessed_news(X) a and sentiment(Y) and split the data in 80:20.
X_train, X_test, y_train, y_test = train_test_split(df['preprocessed_news'], df['sentiment'], test_size=0.2, random_state=42)

# Fit the pipeline on the training data
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

#Now printing the classification report
from sklearn.metrics import classification_report
print("SVM Classification Report:")
print(classification_report(y_test, y_pred))

#accuracy_score comes to be 0.91 for 1000 thousand testing data.

#Checking the overall sentiment
df.prediction.value_counts()
# As from the result one can easily say that it is least likely that the stock price will drop, but it does not give clear verdict on its neutral or increasing nature,so for that we will check average sentiment score



"""NOW SOME VISUALTZATION TO HAVE A BETTER UNDERSTAING OF THE DATA"""

import yfinance as yf
import matplotlib.pyplot as plt

ticker = 'NVDA'
start_date = '2023-12-12'
end_date = '2024-06-06'

data = yf.download(ticker, start=start_date, end=end_date)

# Step 2: Plotting using matplotlib
plt.figure(figsize=(12, 6))

# Plotting closing prices
plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price', marker='o', linestyle='-', color='blue')
plt.title(f'{ticker} Close Price')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)

# Plotting volume
plt.subplot(2, 1, 2)
plt.bar(data.index, data['Volume'], color='orange')
plt.title(f'{ticker} Trading Volume')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.grid(True)

plt.tight_layout()
plt.show()



"""Doing a small portfolio check , just as an random example"""

#Checking average sentiment score of NVDA and check that soes it match actual results or not
# If it is positive it indicate that stock price should move over a period and if it is negative means it's price should drop
mean = df.sentiment_score.mean()
print(mean)
#Result is Mean = 0.12028386, positive , so price should hike ,lets check it through graph

import matplotlib.pyplot as plt

# Initial data
initial_stock_price = 50  # Initial stock price on January 1st, 2024
final_stock_price = 125   # Final stock price on June 30th, 2024
initial_cash = 10000

# Calculations
num_shares = initial_cash / initial_stock_price
final_portfolio_value = num_shares * final_stock_price
total_return = (final_portfolio_value - initial_cash) / initial_cash * 100

# Data for visualization
labels = ['Initial Cash','Final Portfolio Value']
values = [initial_cash,final_portfolio_value]

# Plotting
fig, ax1 = plt.subplots(figsize=(7, 6))

# Primary bar chart for cash and stock prices
bars = ax1.bar(labels, values, color=['blue', 'green', 'red', 'purple'])

# Adding text labels on bars
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom')

# Setting primary y-axis label
ax1.set_ylabel('Values in USD')
ax1.set_title('Stock Investment Summary', fontsize=12)

# Creating secondary y-axis for total return percentage
ax2 = ax1.twinx()
ax2.plot(['Total Return (%)'], [total_return], color='orange', marker='o', markersize=10, linestyle='-', linewidth=2)
ax2.set_ylabel('Total Return (%)')

# Adding text label on the percentage return point
ax2.text(0, total_return, f'{total_return:.2f}%', ha='center', va='bottom', fontsize=12, color='orange')

# Enhancing aesthetics
ax1.grid(True)
ax1.set_facecolor('#f0f0f0')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Showing the plot
plt.show()

# Print results
print(f"Initial cash: ${initial_cash}")
print(f"Initial stock price: ${initial_stock_price}")
print(f"Final stock price: ${final_stock_price}")
print(f"Number of shares purchased: {num_shares:.2f}")
print(f"Final portfolio value: ${final_portfolio_value:.2f}")
print(f"Total return: {total_return:.2f}%")



#Similarly we do our analysis on other stocks as well.

