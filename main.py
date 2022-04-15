import random
import nltk
import json
from sklearn.feature_extraction.text import CountVectorizer


with open ('BOT_CONFIG.json') as f:
  BOT_CONFIG = json.load(f)
# len(BOT_CONFIG['intents'].keys())
# BOT_CONFIG.keys()


texts = []
y = []
for intent in BOT_CONFIG['intents'].keys():
  for examples in BOT_CONFIG['intents'][intent]['examples']:
    texts.append(examples)
    y.append(intent)


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)


vocab = vectorizer.get_feature_names_out()

print (vocab)