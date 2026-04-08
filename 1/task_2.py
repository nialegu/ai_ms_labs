import random

list_of_words = [
    'яблоко', 'победа', 'программирование', 'терминал', 'ноутбук',
    'монитор', 'клавиатура', 'процессор', 'память', 'алгоритм',
    'компьютер', 'интернет', 'разработка', 'программа', 'система'
]

def input_word_from_list():
    while True:
        word = input(f'Выберите слово из списка {list_of_words}: ').lower()
        if word in list_of_words:
            return word
        else:
            print('Слово не из списка, попробуйте снова!')

def display_progress(word, discovered):
    return ' '.join([ch if ch in discovered else '_' for ch in word])

user_word = input_word_from_list()          # слово, которое загадывает игрок
computer_word = random.choice(list_of_words)  # слово компьютера
print('\nКомпьютер загадал своё слово.')

user_discovered = set()       # что игрок угадал в слове компьютера
computer_discovered = set()   # что компьютер угадал в слове игрока
user_health = 5
computer_health = 5

letters_for_computer = list('абвгдеёжзийклмнопрстуфхцчшщьыъэюя')

# игра поочередно
while True:
    # ход игрока
    print('\nВаше слово для угадывания:', display_progress(computer_word, user_discovered))
    while True:
        user_guess = input('Введите букву: ').lower()
        if len(user_guess) != 1:
            print('Введите одну букву!')
            continue
        if user_guess in user_discovered:
            print('Эта буква уже была.')
            continue
        break

    if user_guess in computer_word:
        print('Буква есть!')
        user_discovered.add(user_guess)
    else:
        user_health -= 1
        print(f'Буквы нет. Жизни: {user_health}')

    # проверка победы игрока
    if set(computer_word) == user_discovered:
        print(f'\nВы угадали слово "{computer_word}"! Вы победили!')
        break
    if user_health == 0:
        print(f'\nУ вас закончились жизни. Слово было "{computer_word}".')
        break

    # ход компьютера
    print('\nХод компьютера...')
    available_letters = [ch for ch in letters_for_computer if ch not in computer_discovered]
    if not available_letters:
        print('Компьютер больше не может угадывать буквы.')
        break
    comp_guess = random.choice(available_letters)
    print('Компьютер вводит:', comp_guess)

    if comp_guess in user_word:
        print('Буква есть!')
        computer_discovered.add(comp_guess)
    else:
        computer_health -= 1
        print(f'Буквы нет. Жизни компьютера: {computer_health}')

    # проверка победы компьютера
    if set(user_word) == computer_discovered:
        print(f'\nКомпьютер угадал слово "{user_word}"! Компьютер победил!')
        break
    if computer_health == 0:
        print(f'\nУ компьютера закончились жизни. Слово было "{user_word}".')
        break