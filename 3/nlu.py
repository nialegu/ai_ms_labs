import random
import re

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

BOT_CONFIG = {
    'intents': {
        'greeting': {
            'examples': ['привет', 'здравствуйте', 'добрый день'],
            'responses': ['Здравствуйте', 'Добрый день', 'Привет'],
        },
        'farewell': {
            'examples': ['пока', 'до свидания', 'увидимся'],
            'responses': ['До свидания', 'Всего доброго'],
        },
        'phone_interest': {
            'examples': [
                'хочу купить телефон', 'посоветуй смартфон',
                'какой телефон выбрать', 'нужен смартфон'
            ],
            'responses': [
                'Сейчас популярны iPhone, Samsung Galaxy и Google Pixel. Что интересует?',
                'Могу помочь выбрать смартфон. Какие характеристики важны?'
            ],
        },
        'iphone': {
            'examples': ['iphone', 'айфон', 'iphone 15'],
            'responses': [
                'iPhone отличается стабильной работой и экосистемой Apple.',
                'iPhone 15 Pro предлагает мощный процессор и качественную камеру.'
            ],
        },
        'samsung': {
            'examples': ['samsung', 'galaxy', 's24'],
            'responses': [
                'Samsung Galaxy предлагает отличные дисплеи и универсальность.',
                'Galaxy S24 — один из флагманов с мощной камерой.'
            ],
        },
        'pixel': {
            'examples': ['pixel', 'google pixel'],
            'responses': [
                'Google Pixel известен своей камерой и чистым Android.',
                'Pixel 8 отлично подходит для фото.'
            ],
        },
        'price': {
            'examples': ['цена', 'сколько стоит'],
            'responses': [
                'Цены зависят от модели, но флагманы стоят дороже среднего сегмента.'
            ],
        },
    },
    'failure_phrases': [
        'Не удалось распознать запрос. Попробуйте уточнить.',
        'Не совсем понятно. Задайте вопрос иначе.'
    ]
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^а-яёa-z\s]', '', text)
    return text.strip()


class IntentModel:
    def __init__(self, config):
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        self.model = LinearSVC()
        self._train(config)

    def _train(self, config):
        X = []
        y = []

        for intent, data in config['intents'].items():
            for example in data['examples']:
                X.append(clean_text(example))
                y.append(intent)

        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)

    def predict(self, text: str):
        text = clean_text(text)
        if not text:
            return None

        vec = self.vectorizer.transform([text])
        return self.model.predict(vec)[0]


_model = IntentModel(BOT_CONFIG)


def classify_intent(text: str):
    return _model.predict(text)


def get_answer_by_intent(intent: str):
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])


def get_failure_phrase():
    return random.choice(BOT_CONFIG['failure_phrases'])