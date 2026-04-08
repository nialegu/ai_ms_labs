import math

def solve_quadratic(a, b, c):
    # Формируем строку уравнения для наглядности
    equation = ""
    if a != 0:
        equation += f"{a}x²"
    if b != 0:
        equation += f" + {b}x" if b > 0 else f" - {-b}x"
    if c != 0:
        equation += f" + {c}" if c > 0 else f" - {-c}"
    equation += " = 0"
    
    print(f"\nРассматриваем уравнение: {equation}\n")
    
    # Если a = 0, уравнение не квадратное
    if a == 0:
        if b == 0:
            if c == 0:
                return "Уравнение имеет бесконечно много решений (0=0)."
            else:
                return "Уравнение не имеет решений."
        else:
            # Линейное уравнение bx + c = 0
            x = -c / b
            return f"Линейное уравнение. Корень: x = {x}"
    
    # Дискриминант
    D = b**2 - 4*a*c

    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        return f"Два действительных корня: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2*a)
        return f"Один действительный корень: x = {x}"
    else:
        # Комплексные корни
        real_part = -b / (2*a)
        imag_part = math.sqrt(-D) / (2*a)
        return f"Два комплексных корня: x1 = {real_part}+{imag_part}i, x2 = {real_part}-{imag_part}i"

# Ввод коэффициентов
try:
    a = float(input("Введите коэффициент a: "))
    b = float(input("Введите коэффициент b: "))
    c = float(input("Введите коэффициент c: "))
except ValueError:
    print("Некорректный ввод. Введите числа.")
else:
    result = solve_quadratic(a, b, c)
    print(result)
