import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
n = 12          # число источников
k = 5           # заявок в месяц
t = 0.8         # время обслуживания (дни)
P_required = 85 # требуемый процент

# Основные параметры

# Интенсивность потока от одного источника
lam = k / 30

# Интенсивность обслуживания
mu = 1 / t

# Приведенная интенсивность
rho = lam / mu
print("Основные параметры:")
print(f"λ = {lam:.5f}")
print(f"μ = {mu:.5f}")
print(f"ρ = {rho:.5f}")

# Вероятность p0
s = 0
for i in range(n + 1):
    s += (math.factorial(n) /
          math.factorial(n - i)) * \
         (rho ** i)
p0 = 1 / s
print(f"\np0 = {p0:.5f}")

# Вероятности состояний
states = []
probs = []
for i in range(n + 1):
    pi = (math.factorial(n) /
          math.factorial(n - i)) * \
         (rho ** i) * p0
    states.append(f"S{i}")
    probs.append(pi)

# Таблица вероятностей
df = pd.DataFrame({
    "State": states,
    "Probability": probs
})
print("\nВероятности состояний:")
print(df)

# Среднее число заявок в системе
L_system = 0
for i in range(n + 1):
    L_system += i * probs[i]
print(f"\nLсист = {L_system:.5f}")

# Активные источники
active_sources = n - L_system
active_percent = \
    active_sources / n * 100
print(f"\nАктивные источники = {active_sources:.5f}")
print(f"Процент активности = {active_percent:.2f}%")

# Абсолютная пропускная способность
A = mu * (1 - p0)
print(f"\nАбсолютная пропускная способность = {A:.5f}")

# Временные характеристики
T_system = L_system / A
T_wait = T_system - t
print(f"\nTсист = {T_system:.5f}")
print(f"Tож = {T_wait:.5f}")

# Проверка условия
if active_percent >= P_required:
    print("\nУсловие выполняется")
else:
    print("\nУсловие НЕ выполняется")

# График вероятностей
plt.figure(figsize=(12, 5))
plt.bar(states, probs)
plt.title("Вероятности состояний")
plt.xlabel("Состояния")
plt.ylabel("Вероятность")
plt.grid(True)
plt.show()