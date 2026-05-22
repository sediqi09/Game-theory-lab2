import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
lam = 0.7       # заявок в минуту
t_service = 3.5 # минут
k = 4           # число каналов
omega = 10      # допустимое время ожидания
C = 280         # доход от заявки
eps = 0.01      # точность

# Основные параметры
mu = 1 / t_service
rho = lam / mu
psi = rho / k

print("Основные параметры:")
print(f"μ = {mu:.5f}")
print(f"ρ = {rho:.5f}")
print(f"ψ = {psi:.5f}")

# Вероятность свободной системы
sum1 = 0
for i in range(k):
    sum1 += (rho ** i) / math.factorial(i)
sum2 = ((rho ** k) /
        math.factorial(k)) * \
       (1 / (1 - psi))
p0 = 1 / (sum1 + sum2)
print(f"\np0 = {p0:.5f}")

# Вероятность ожидания
P_queue = ((rho ** k) /
           math.factorial(k)) * \
          p0 / (1 - psi)

print(f"Pоч = {P_queue:.5f}")

# Среднее число заявок
L_queue = ((rho ** (k + 1)) /
           (k * math.factorial(k))) * \
          p0 / ((1 - psi) ** 2)
L_system = L_queue + rho
print(f"Lоч = {L_queue:.5f}")
print(f"Lсист = {L_system:.5f}")

# Временные характеристики
T_queue = L_queue / lam
T_system = L_system / lam
print(f"Tоч = {T_queue:.5f}")
print(f"Tсист = {T_system:.5f}")

# Вероятность ухода
P_leave = 1 - math.exp(-T_queue / omega)
P_service = 1 - P_leave
print(f"\nPуход = {P_leave:.5f}")
print(f"Pобсл = {P_service:.5f}")

# Потери дохода
nu_leave = lam * P_leave
Loss = C * nu_leave
print(f"\nПотери дохода = {Loss:.5f}")

# Таблица результатов
results = pd.DataFrame({

    "Параметр": [
        "ρ",
        "p0",
        "Pоч",
        "Lоч",
        "Lсист",
        "Tоч",
        "Tсист",
        "Pобсл",
        "Потери"
    ],

    "Значение": [
        rho,
        p0,
        P_queue,
        L_queue,
        L_system,
        T_queue,
        T_system,
        P_service,
        Loss
    ]
})
print("\nТаблица результатов:")
print(results)

# График характеристик
plt.figure(figsize=(10, 5))
plt.bar(
    results["Параметр"],
    results["Значение"]
)
plt.title("Основные характеристики СМО")
plt.grid(True)
plt.show()