import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
k = 5       # число каналов
n = 18      # число источников
lam = 1.0   # интенсивность потока
t = 0.2     # время обслуживания (час)

# Основные параметры
mu = 1 / t
rho = lam / mu
print("Основные параметры:")
print(f"μ = {mu:.5f}")
print(f"ρ = {rho:.5f}")

# Вероятность p0
s = 0
for i in range(n + 1):
    if i <= k:
        term = (
            math.factorial(n) /
            math.factorial(n - i)
        ) * (rho ** i) / math.factorial(i)

    else:
        term = (
            math.factorial(n) /
            math.factorial(n - i)
        ) * (rho ** i) / \
               (math.factorial(k) *
                (k ** (i - k)))
    s += term
p0 = 1 / s
print(f"\np0 = {p0:.5f}")

# Вероятности состояний
states = []
probs = []
for i in range(n + 1):
    if i <= k:
        pi = (
            math.factorial(n) /
            math.factorial(n - i)
        ) * (rho ** i) / \
             math.factorial(i) * p0

    else:
        pi = (
            math.factorial(n) /
            math.factorial(n - i)
        ) * (rho ** i) / \
             (math.factorial(k) *
              (k ** (i - k))) * p0
    states.append(f"S{i}")
    probs.append(pi)

# Таблица вероятностей
df = pd.DataFrame({
    "State": states,
    "Probability": probs
})
print("\nТаблица вероятностей:")
print(df)

# Средние характеристики
L_system = 0
for i in range(n + 1):
    L_system += i * probs[i]
L_queue = 0
for i in range(k + 1, n + 1):
    L_queue += (i - k) * probs[i]
L_busy = L_system - L_queue
L_free = k - L_busy

# Пропускная способность
A = mu * L_busy
Q = A / (n * lam)

# Вероятность очереди
P_queue = sum(probs[k + 1:])

# Временные характеристики
T_queue = L_queue / A
T_system = L_system / A

# Вывод результатов
print("\nОсновные характеристики:")
print(f"Lоч = {L_queue:.5f}")
print(f"Lсист = {L_system:.5f}")
print(f"Lсвоб = {L_free:.5f}")
print(f"Lзан = {L_busy:.5f}")
print(f"A = {A:.5f}")
print(f"Q = {Q:.5f}")
print(f"Pоч = {P_queue:.5f}")
print(f"Tоч = {T_queue:.5f} ч")
print(f"Tсист = {T_system:.5f} ч")

# График вероятностей
plt.figure(figsize=(14, 5))
plt.bar(states, probs)
plt.title("Вероятности состояний")
plt.xlabel("Состояния")
plt.ylabel("Вероятность")
plt.grid(True)
plt.show()