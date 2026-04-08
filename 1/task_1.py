import random

def input_number(message):
    while True:
        try:
            num = int(input(message))
            if 1 <= num <= 100:
                return num
            else:
                print('Введите число от 1 до 100!')
        except ValueError:
            print('Введите корректное число!')

random_number = random.randint(1, 100)
print('Компьютер загадал число от 1 до 100!')

low = 1
high = 100

user_number = input_number('Вы загадываете число: ')

while True:

    # Ход игрока
    user_guess = input_number('Ваш ход: ')

    if user_guess == random_number:
        print('Вы угадали! Победа игрока!')
        break
    elif user_guess < random_number:
        print('Больше!')
    else:
        print('Меньше!')

    # Ход компьютера
    if low > high:
        print('Ошибка диапазона угадывания компьютера.')
        break

    comp_guess = random.randint(low, high)
    print('Ход компьютера:', comp_guess)

    if comp_guess == user_number:
        print('Компьютер угадал! Победа компьютера!')
        break
    elif comp_guess < user_number:
        print('Для компьютера: больше')
        low = comp_guess + 1
    else:
        print('Для компьютера: меньше')
        high = comp_guess - 1