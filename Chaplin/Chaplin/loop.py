import shelve, config, db
from pymorphy2 import MorphAnalyzer
from kb import knowledge_base
from chaplin import chatbot

def makeRequest(words, morph):
    for i in range(len(words)):
        words[i] = morph.normal_forms(words[i])[0]
    return words

if __name__ == '__main__':
    data = shelve.open(config.DB_NAME)
    base = knowledge_base()
    morph = MorphAnalyzer()
    chaplin = chatbot(data, base, morph)
    msg = []
    while True:
        chaplin.chat(msg)
        print('    Вы: ', end='')
        msg = input()
        msg = knowledge_base.split_words(msg)
        msg = makeRequest(msg, morph)
