import math

def triangle_type(a, b, c):
    # Проверка возможности существования треугольника
    sides = sorted([a, b, c])
    if sides[0] + sides[1] <= sides[2]:
        return "Треугольник с такими сторонами не существует."

    # Определяем углы с помощью теоремы косинусов
    a2, b2, c2 = sides[0]**2, sides[1]**2, sides[2]**2

    if math.isclose(a2 + b2, c2):
        angle_type = "прямоугольный"
    elif a2 + b2 > c2:
        angle_type = "остроугольный"
    else:
        angle_type = "тупоугольный"

    # Определяем тип по сторонам
    if math.isclose(a, b) and math.isclose(b, c):
        side_type = "равносторонний"
    elif math.isclose(a, b) or math.isclose(a, c) or math.isclose(b, c):
        side_type = "равнобедренный"
    else:
        side_type = "разносторонний"

    return f"Треугольник {side_type}-{angle_type}."

# Ввод сторон треугольника
try:
    a = float(input("Введите сторону a: "))
    b = float(input("Введите сторону b: "))
    c = float(input("Введите сторону c: "))
except ValueError:
    print("Некорректный ввод. Введите числа.")
else:
    result = triangle_type(a, b, c)
    print(result)
