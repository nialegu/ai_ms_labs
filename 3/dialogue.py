import os
import random
import nltk

from nlu import clean_text

PRODUCTS = [
    {
        'name': 'iPhone 15 Pro',
        'brand': 'Apple',
        'price': 'from 999$',
        'desc': 'High performance and premium camera',
        'keywords': {'iphone', 'apple'},
    },
    {
        'name': 'Samsung Galaxy S24',
        'brand': 'Samsung',
        'price': 'from 899$',
        'desc': 'Top display and flexibility',
        'keywords': {'samsung', 'galaxy'},
    },
    {
        'name': 'Google Pixel 8',
        'brand': 'Google',
        'price': 'from 799$',
        'desc': 'Best camera and clean Android',
        'keywords': {'pixel', 'google'},
    },
]


class DialogueGenerator:
    def __init__(self, path):
        self.data = []
        self._load(path)

    def _load(self, path):
        if not os.path.exists(path):
            return

        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n\n')

        for block in lines:
            parts = block.split('\n')
            if len(parts) == 2:
                q = clean_text(parts[0])
                a = parts[1]
                self.data.append((q, a))

    def generate_answer(self, text):
        text = clean_text(text)
        best = None

        for q, a in self.data:
            dist = nltk.edit_distance(text, q)
            if dist < 5:
                best = a

        return best


def get_random_product():
    return random.choice(PRODUCTS)


def format_product(product):
    return f"{product['name']} ({product['brand']})\n{product['price']}\n{product['desc']}"


def check_ad_trigger(text, intent, count, last):
    if count - last < 5:
        return None, None

    product = get_random_product()
    return format_product(product), 'periodic'