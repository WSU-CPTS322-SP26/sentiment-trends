from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore[import-untyped]


sia = SentimentIntensityAnalyzer()

text = "Vader sentiment is working"
print (text)
print(sia.polarity_scores(text))