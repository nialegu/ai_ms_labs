def isPrime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(3, int(x**0.5) + 1, 2):
        if x % i == 0:
            return False
    return True

def nearestPrime(x):
    if x < 2:
        return 2
    lower = x - 1
    upper = x + 1
    while True:
        if isPrime(lower):
            return lower
        if isPrime(upper):
            return upper
        lower -= 1
        upper += 1

num = int(input("Введите число для проверки: "))

if isPrime(num):
    print(f"{num} — простое число!")
else:
    print(f"{num} — не простое число.")
    print(f"Ближайшее простое число: {nearestPrime(num)}")