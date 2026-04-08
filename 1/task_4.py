from random import choice

options = ["Камень", "Бумага", "Ножницы", "Колодец"]

print("Игра Камень, Ножницы, Бумага, Колодец!")
print("Правила: Бумага побеждает Колодец, Колодец побеждает Камень и Ножницы.")

while True:
    player = input("Выберите Камень, Бумага, Ножницы или Колодец (q для выхода): ")

    if player.lower() == 'q':
        print("Выход из игры.")
        break

    if player not in options:
        print("Некорректный ход! Попробуйте снова.")
        continue

    computer = choice(options)
    print(f"Компьютер выбрал: {computer}")

    if player == computer:
        print("Ничья!")
    elif player == "Камень":
        if computer in ["Ножницы"]:
            print("Ты выиграл! Камень разбивает", computer)
        elif computer in ["Бумага"]:
            print("Ты проиграл! Бумага накрывает Камень")
        elif computer == "Колодец":
            print("Ты проиграл! Камень тонет в Колодце")
    elif player == "Ножницы":
        if computer in ["Бумага"]:
            print("Ты выиграл! Ножницы режут Бумагу")
        elif computer in ["Камень"]:
            print("Ты проиграл! Камень разбивает Ножницы")
        elif computer == "Колодец":
            print("Ты проиграл! Ножницы тонут в Колодце")
    elif player == "Бумага":
        if computer in ["Камень", "Колодец"]:
            print("Ты выиграл!", player, "накрывает", computer)
        elif computer == "Ножницы":
            print("Ты проиграл! Ножницы режут Бумагу")
    elif player == "Колодец":
        if computer in ["Камень", "Ножницы"]:
            print("Ты выиграл! Колодец тонет", computer)
        elif computer == "Бумага":
            print("Ты проиграл! Бумага накрывает Колодец")
        elif computer == "Колодец":
            print("Ничья!")