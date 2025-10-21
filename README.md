
**📈 Stock Sentiment Analysis using News Headlines**

This project performs sentiment analysis on stock market news to predict potential price movement trends based on news sentiment.
It combines web scraping, natural language processing (NLP), and machine learning (SVM with TF-IDF) to determine whether the overall news sentiment around a stock is positive, negative, or neutral, and how that may influence its price.

**🧠 Overview**

Stock prices are highly influenced by investor sentiment and public news.
This project collects recent news articles for a given stock (e.g., NVIDIA – NVDA) and analyzes the tone of each headline to predict whether the stock’s price is likely to:

📈 Rise (Positive)

📉 Fall (Negative)

⚖️ Stay stable (Neutral)

The model then validates this sentiment against real market data to see how closely the sentiment aligns with price trends.

**🗂️ Workflow**

**1. 📰 Data Collection**

News headlines are scraped from Business Insider – Markets.

The script loops through 100 pages of articles for a given stock (e.g., NVDA).

Extracted attributes include:

date_time

source

title

The collected data is stored in:

nvda_news_articles.csv

**2. 🧹 Data Preprocessing**

Clean and normalize text using:

Regex (to remove URLs, numbers, special characters)

SpaCy for tokenization and lemmatization

NLTK for stopword removal and stemming

Processed text is saved in a new column:

preprocessed_news

**3. 💬 Sentiment Analysis**

Sentiment detection is performed using VADER Sentiment Analyzer:

Calculates compound sentiment scores for each headline.

Classifies them as:

Positive

Negative

Neutral

Maps them numerically:

Positive → +1
Neutral  →  0
Negative → -1


Also predicts likely price movement:

Positive → “Price Hike”

Negative → “Price Drop”

Neutral → “No Change”

**4. 🤖 Model Training**

Uses a Support Vector Machine (SVM) classifier with TF-IDF Vectorization in a pipeline:

TF-IDF → SVM


Splits data (80:20) into training and test sets.

Achieves an accuracy of ~91% on the test set.

Displays a classification report with precision, recall, and F1-score.

**5. 📊 Visualization**

Uses yfinance to fetch real NVDA stock data from Dec 2023 to June 2024.

Plots:

Stock Closing Price over time

Stock Trading Volume

Example:

plt.plot(data['Close'], label='Close Price')
plt.bar(data.index, data['Volume'])

**6. 💼 Portfolio Simulation**

Demonstrates a simple investment scenario to compare model sentiment vs. actual price change.

Example:

Initial cash: $10,000
Initial stock price: $50
Final stock price: $125
Total return: 150%


Visualized using a comparative bar and line chart of returns.

**🧰 Tools & Libraries**
Category	Libraries Used
Web Scraping	BeautifulSoup, urllib
Data Handling	pandas, numpy
NLP	spaCy, NLTK, VADER
ML	scikit-learn
Visualization	matplotlib
Financial Data	yfinance


**📈 Results**

Scraped over 100 pages of NVDA stock news

Model accuracy: ~91%

Mean sentiment score: +0.12 (positive) → consistent with NVDA’s price increase trend

Predicted market outlook: Price likely to rise

**🔮 Future Enhancements**

Expand to multiple stocks automatically

Integrate live news feeds & APIs (e.g., Google News API, Reddit, Twitter)

Add LSTM or Transformer models for deeper contextual understanding

Create a Streamlit dashboard for real-time sentiment visualization

**👨‍💻 Author**

Lalit Jingar
📧 lalitjingar90@gmail.com
🌐 linkedin.com/in/lalit-jingar/
⭐ If you like this project, consider giving it a star on GitHub!
