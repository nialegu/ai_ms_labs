def fibSequence(n):
    assert n > 0, "Число должно быть больше нуля"

    series = [1]
    while len(series) < n:
        if len(series) == 1:
            series.append(1)
        else:
            series.append(series[-1] + series[-2])

    return ', '.join(str(num) for num in series)


def fibRecurse(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibRecurse(n - 1) + fibRecurse(n - 2)


num = int(input("Сколько чисел Фибоначчи вывести? "))

print("Ряд Фибоначчи (итеративно):", fibSequence(num))

print("Ряд Фибоначчи (рекурсивно):", ', '.join(str(fibRecurse(i)) for i in range(1, num + 1)))