BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': ['привет', 'прив.'],
            'responses': ['здравствуйте', 'здоров.']
        },
        'bye': {
            'examples': ['пока', 'прощай', 'до свидания'],
            'responses': ['увидимся', 'бывай', 'до связи']
        }
        
    }
}

def get_intent(text):
    for intent in BOT_CONFIG['intents'].keys():
        print(intent)
        for example in BOT_CONFIG['intents'][intent]['examples']:
            print(example)

get_intent('dsads')