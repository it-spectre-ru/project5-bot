import random
import nltk
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split




def clean(text):
  clean_text = ''
  for ch in text.lower():
    if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
      clean_text = clean_text + ch
  return clean_text


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


train_texts, test_texts, y_train, y_test = train_test_split(texts, y, random_state=42, test_size=0.32)


vectorizer = CountVectorizer(ngram_range=(1,3), analyzer='char_wb') #TfidfVectorizer(ngram_range=(1,5), analyzer='char_wb')  
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)


vocab = vectorizer.get_feature_names_out()


# len(vocab)
# vocab


clf = RandomForestClassifier(n_estimators=300).fit(X_train, y_train)  #LogisticRegression().fit(X_train, y_train) #LogisticRegression(C=2) штрафует модель за зазубривание
clf.score(X_train, y_train), clf.score(X_test, y_test)


clf.predict(vectorizer.transform(['заказ']))


BOT_CONFIG['intents']['zamer']


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