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


# загрузил из json все интенты
with open ('BOT_CONFIG.json') as f:
  BOT_CONFIG = json.load(f)
# len(BOT_CONFIG['intents'].keys())
# BOT_CONFIG.keys()


# все тексты в список texts
# все интенты этих текстов в список y 
texts = []
y = []
for intent in BOT_CONFIG['intents'].keys():
  for examples in BOT_CONFIG['intents'][intent]['examples']:
    texts.append(examples)
    y.append(intent)


# разбил на обучающую и тестовую часть
train_texts, test_texts, y_train, y_test = train_test_split(texts, y, random_state=42, test_size=0.32)


# обучил vectorizer
vectorizer = CountVectorizer(ngram_range=(1,3), analyzer='word') #TfidfVectorizer(ngram_range=(1,5), analyzer='char_wb')  
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)


vocab = vectorizer.get_feature_names_out()


len(vocab)
vocab


# обучил классиикатор
# получил точность на обучающей части и на тестовой
clf = LogisticRegression().fit(X_train, y_train) #RandomForestClassifier(n_estimators=300).fit(X_train, y_train)   #LogisticRegression(C=2) штрафует модель за зазубривание
clf.score(X_train, y_train), clf.score(X_test, y_test)


clf.predict(vectorizer.transform(['Привет!']))


BOT_CONFIG['intents']['zamer']


def get_intent_by_model(text):
  return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
  intent = get_intent_by_model(input_text)
  return random.choice(BOT_CONFIG['intents'][intent]['responses'])
  

# input_text = ''
# while input_text != 'stop':
#   input_text = input()
#   if input_text != 'stop':
#     response = bot(input_text)
#     print(response)



import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    input_text = update.message.text
    output_text = bot(input_text)
    
    update.message.reply_text(output_text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5231507466:AAHZ8799BQRbV9eU6AsIUANxmP5-nIs7Pkw")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()