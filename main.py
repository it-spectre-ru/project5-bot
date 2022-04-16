import random
import nltk
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression



with open ('BOT_CONFIG.json') as f:
  BOT_CONFIG = json.load(f)


texts = []
y = []
for intent in BOT_CONFIG['intents'].keys():
  for examples in BOT_CONFIG['intents'][intent]['examples']:
    texts.append(examples)
    y.append(intent)


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)


vocab = vectorizer.get_feature_names_out()


clf = LogisticRegression().fit(X, y)
clf.score(X, y)


def clean(text):
  clean_text = ''
  for ch in text.lower():
    if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
      clean_text = clean_text + ch
  return clean_text


def get_intent_by_model(text):
  return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
  intent = get_intent_by_model(input_text)
  return random.choice(BOT_CONFIG['intents'][intent]['responses'])


input_text = ''
while input_text != 'stop':
  input_text = input()
  if input_text != 'stop':
    response = bot(input_text)
    print(response) 
  
