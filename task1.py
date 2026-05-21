import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
alpha = 1.2          # среднее время обслуживания (час)
n_day = 60           # заявок в сутки
k = 5                # число каналов

# Основные параметры

# интенсивность потока заявок
lam = n_day / 24

# интенсивность обслуживания
mu = 1 / alpha

# приведенная интенсивность
rho = lam / mu

print(f"λ = {lam:.3f}")
print(f"μ = {mu:.3f}")
print(f"ρ = {rho:.3f}")

# Функция вычисления p0
def calc_p0(rho, channels):
    s = 0
    for i in range(channels + 1):
        s += (rho ** i) / math.factorial(i)
    return 1 / s

# Минимальное число каналов
channels = 1

while True:

    p0 = calc_p0(rho, channels)

    p_fail = ((rho ** channels) /
              math.factorial(channels)) * p0

    Q = 1 - p_fail

    if Q >= 0.95:
        break

    channels += 1

print("\nМинимальное число каналов:")
print(channels)

# Расчет для k = 5
p0 = calc_p0(rho, k)

# вероятности состояний
probabilities = []

for i in range(k + 1):

    pi = ((rho ** i) /
          math.factorial(i)) * p0

    probabilities.append(pi)

# характеристики системы
p_fail = probabilities[k]
Q = 1 - p_fail
A = lam * Q
k_avg = rho * Q
load_coeff = k_avg / k

# Таблица вероятностей
table = pd.DataFrame({
    "Состояние": [f"S{i}" for i in range(k + 1)],
    "Вероятность": probabilities
})

print("\nВероятности состояний:")
print(table)

# Основные характеристики
print("\nОсновные характеристики:")
print(f"Вероятность отказа = {p_fail:.4f}")
print(f"Относительная пропускная способность Q = {Q:.4f}")
print(f"Абсолютная пропускная способность A = {A:.4f}")
print(f"Среднее число занятых каналов = {k_avg:.4f}")
print(f"Коэффициент загрузки = {load_coeff:.4f}")

# График вероятностей
plt.figure(figsize=(8, 5))
plt.bar(
    [f"S{i}" for i in range(k + 1)],
    probabilities
)
plt.title("Вероятности состояний СМО")
plt.xlabel("Состояния")
plt.ylabel("Вероятность")
plt.grid(True)
plt.show()