import random

# Функция рисования поля
def draw_board(board, size):
    print("-" * (size * 4 + 1))
    for i in range(size):
        row = "| "
        for j in range(size):
            row += str(board[i * size + j]) + " | "
        print(row)
        print("-" * (size * 4 + 1))

# Ввод хода игрока
def take_input(board, player_token, size):
    valid = False
    while not valid:
        player_answer = input(f"Куда поставим {player_token}? ")
        try:
            player_answer = int(player_answer)
        except:
            print("Некорректный ввод. Введите число.")
            continue
        if 1 <= player_answer <= size**2:
            if str(board[player_answer - 1]) not in "XO":
                board[player_answer - 1] = player_token
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print(f"Некорректный ввод. Введите число от 1 до {size**2}.")

# Проверка победителя
def check_win(board, size):
    # строки
    for i in range(size):
        if board[i*size:(i+1)*size].count(board[i*size]) == size and board[i*size] in "XO":
            return board[i*size]
    # столбцы
    for j in range(size):
        col = [board[j + i*size] for i in range(size)]
        if col.count(col[0]) == size and col[0] in "XO":
            return col[0]
    # диагонали
    diag1 = [board[i*(size+1)] for i in range(size)]
    diag2 = [board[(i+1)*(size-1)] for i in range(size)]
    if diag1.count(diag1[0]) == size and diag1[0] in "XO":
        return diag1[0]
    if diag2.count(diag2[0]) == size and diag2[0] in "XO":
        return diag2[0]
    return False

# Игра 5x5 для двух игроков
def game_5x5():
    size = 5
    board = list(range(1, size*size + 1))
    counter = 0
    win = False
    while not win:
        draw_board(board, size)
        if counter % 2 == 0:
            take_input(board, "X", size)
        else:
            take_input(board, "O", size)
        counter += 1
        if counter >= 9:
            tmp = check_win(board, size)
            if tmp:
                draw_board(board, size)
                print(tmp, "выиграл!")
                return
        if counter == size*size:
            draw_board(board, size)
            print("Ничья!")
            return

# Игра 3x3 против компьютера
def game_3x3_vs_bot():
    size = 3
    board = list(range(1, size*size + 1))
    counter = 0
    win = False
    while not win:
        draw_board(board, size)
        if counter % 2 == 0:
            take_input(board, "X", size)
        else:
            # Ход компьютера
            empty_cells = [i for i, v in enumerate(board) if str(v) not in "XO"]
            bot_choice = random.choice(empty_cells)
            board[bot_choice] = "O"
            print(f"Компьютер поставил O в клетку {bot_choice+1}")
        counter += 1
        if counter >= 5:
            tmp = check_win(board, size)
            if tmp:
                draw_board(board, size)
                print(tmp, "выиграл!")
                return
        if counter == size*size:
            draw_board(board, size)
            print("Ничья!")
            return

# Главное меню
print("Выберите режим игры:")
print("1 - Два игрока (5x5)")
print("2 - Игрок против компьютера (3x3)")
mode = input("Ваш выбор: ")

if mode == "1":
    game_5x5()
elif mode == "2":
    game_3x3_vs_bot()
else:
    print("Некорректный выбор.")

input("Нажмите Enter для выхода!")