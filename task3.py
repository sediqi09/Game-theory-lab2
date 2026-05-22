import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
lam = 4          # заявок в час
t_service = 2    # минут
k = 10           # число каналов
n = 4            # мест в очереди
T = 10           # часов работы
C = 80           # стоимость заявки

# Основные параметры
mu = 60 / t_service
rho = lam / mu
psi = rho / k

print(f"μ = {mu:.4f}")
print(f"ρ = {rho:.4f}")
print(f"ψ = {psi:.6f}")

# Вероятность p0
sum1 = 0
for i in range(k + 1):
    sum1 += (rho ** i) / math.factorial(i)
sum2 = ((rho ** (k + 1)) /
        (math.factorial(k) * k))
sum2 *= ((1 - (rho / k) ** n) /
         (1 - rho / k))
p0 = 1 / (sum1 + sum2)
print(f"\np0 = {p0:.6f}")

# Вероятности состояний
states = []
probs = []

# состояния без очереди
for i in range(k + 1):

    pi = ((rho ** i) /
          math.factorial(i)) * p0

    states.append(f"S{i}")
    probs.append(pi)

# состояния очереди
for r in range(1, n + 1):

    pi = ((rho ** (k + r)) /
          (math.factorial(k) * (k ** r))) * p0

    states.append(f"S{k+r}")
    probs.append(pi)

# Таблица вероятностей
df = pd.DataFrame({
    "State": states,
    "Probability": probs
})

print("\nТаблица вероятностей:")
print(df)

# Вероятность отказа
P_fail = probs[-1]
Q = 1 - P_fail
A = lam * Q

# Средние характеристики
L_service = rho * Q
L_queue = 0
for r in range(1, n + 1):
    pi = probs[k + r]
    L_queue += r * pi
L_system = L_service + L_queue

# Временные характеристики
T_queue = L_queue / A
T_system = L_system / A

# Потери выручки
Loss = C * lam * P_fail * T

# Вывод результатов
print("\nОсновные характеристики:")
print(f"Pотк = {P_fail:.10f}")
print(f"Q = {Q:.10f}")
print(f"A = {A:.4f}")
print(f"Lоч = {L_queue:.10f}")
print(f"Lоб = {L_service:.4f}")
print(f"Lсист = {L_system:.4f}")
print(f"Tоч = {T_queue:.10f} ч")
print(f"Tсист = {T_system:.6f} ч")
print(f"Потери = {Loss:.10f}")

# График вероятностей
plt.figure(figsize=(12, 5))
plt.bar(states, probs)
plt.title("Вероятности состояний")
plt.xlabel("Состояния")
plt.ylabel("Вероятность")
plt.grid(True)
plt.show()