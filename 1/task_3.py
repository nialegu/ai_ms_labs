import random

def generate_password():
    password = []

    for i in range(random.randint(2, 4)):
        password.append(chr(random.randint(65, 90)))  # uppercase

    for i in range(random.randint(2, 4)):
        password.append(chr(random.randint(97, 122)))  # lowercase

    for i in range(random.randint(2, 4)):
        password.append(chr(random.randint(48, 57)))  # digits

    special_ranges = list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 127))
    for i in range(random.randint(2, 4)):
        password.append(chr(random.choice(special_ranges)))

    random.shuffle(password)

    return ''.join(password)


# Основная программа
with open("passwords.txt", "a", encoding="utf-8") as file:
    while True:
        site = input("Введите сайт (или q для выхода): ")

        if site.lower() == 'q':
            print("Выход из программы.")
            break

        login = input("Введите логин: ")

        password = generate_password()

        print(f"Сгенерированный пароль: {password}")

        # запись в файл
        file.write(f"{site} - {login} - {password}\n")