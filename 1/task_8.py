import random
import time
import os

score_player = 0
score_bot = 0

all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

bot_skill = float(input("Введите уровень сложности бота (0-1): "))

print("Поиграем в 21? \nЕсли хотите играть нажмите Enter, если хотите выйти, то Ctrl+C")
input()

while True:
    if score_player == 21:
        print("Больше карт не надо, у вас 21")
        print("Вы автоматически победили бота!")
        input("Нажмите Enter, чтобы закрыть окно.")
        break
    if score_player > 21:
        print("Вы проиграли, так как набрали больше 21")
        input("Нажмите Enter, чтобы закрыть окно.")
        break

    yes_or_no = input("Будете ли вы брать карту? (yes/no): ").lower()
    os.system('cls' if os.name == 'nt' else 'clear')

    if yes_or_no == 'yes':
        card = random.choice(all_cards)
        score_player += card
        print(f"Вы взяли карту: {card}")
        print(f"Сейчас у вас {score_player} очков")
    elif yes_or_no == 'no':
        print(f"У вас {score_player} очков.")
        print("Ход бота...")
        time.sleep(2)

        while True:
            needed = score_player + 1 - score_bot
            if needed <= 11 and random.random() < bot_skill:
                card = needed
            else:
                card = random.choice(all_cards)

            score_bot += card
            print(f"Бот берет карту: {card}")
            print(f"У бота {score_bot} очков")
            time.sleep(2)

            if score_bot > 21:
                print(f"Бот проиграл! У него {score_bot} очков, у вас {score_player}")
                input("Нажмите Enter, чтобы закрыть игру.")
                exit(0)
            elif score_bot > score_player:
                print(f"Бот победил! У него {score_bot} очков, у вас {score_player}")
                input("Нажмите Enter, чтобы закрыть игру.")
                exit(0)
            elif score_bot == score_player:
                print(f"Ничья! У вас и бота {score_player} очков")
                input("Нажмите Enter, чтобы закрыть игру.")
                exit(0)