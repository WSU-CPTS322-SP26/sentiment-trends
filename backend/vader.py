from nltk.sentiment import SentimentIntensityAnalyzer


sia = SentimentIntensityAnalyzer()

text = "Vader sentiment is working"
print (text)
print(sia.polarity_scores(text))

