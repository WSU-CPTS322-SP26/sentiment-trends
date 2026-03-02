from nltk.sentiment import SentimentIntensityAnalyzer


sia = SentimentIntensityAnalyzer()

text = "Vader sentiment is working. I'm excited"
print (text)
print(sia.polarity_scores(text))


text = "Vader sentiment is not working and I'm upset about it!"
print (text)
print(sia.polarity_scores(text))