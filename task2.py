import math
import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
# Интенсивность входящего потока
# 125 заявок в сутки
lambda_day = 125

# Среднее время обслуживания (мин)
t_service = 4

# Коэффициент стоимости ожидания
alpha = 8

# Максимальное количество заявок в очереди
n_limit = 4

# Приведение единиц измерения
# λ — заявок в минуту
lam = lambda_day / (24 * 60)

# μ — интенсивность обслуживания
mu = 1 / t_service

# Приведенная интенсивность
rho = lam / mu

print("Исходные параметры:")
print(f"λ = {lam:.5f} заяв/мин")
print(f"μ = {mu:.5f} заяв/мин")
print(f"ρ = {rho:.5f}")

# 1. Минимальное количество каналов
k_min = math.floor(rho) + 1

print("\nМинимальное число каналов:")
print(f"k_min = {k_min}")

# Функции для многоканальной СМО
def calc_p0(rho, k):

    """
    Вероятность свободной системы
    """

    psi = rho / k

    s = 0

    # Сумма первой части
    for i in range(k):
        s += (rho ** i) / math.factorial(i)

    # Последний член
    s += ((rho ** k) /
          math.factorial(k)) * (1 / (1 - psi))

    return 1 / s


def calc_characteristics(k):

    """
    Расчет характеристик СМО
    """

    psi = rho / k

    p0 = calc_p0(rho, k)

    # Вероятность ожидания
    p_queue = ((rho ** k) /
               math.factorial(k)) * \
              p0 / (1 - psi)

    # Среднее число заявок в очереди
    Lq = ((rho ** (k + 1)) /
          (k * math.factorial(k))) * \
         p0 / ((1 - psi) ** 2)

    # Среднее число заявок в системе
    Ls = Lq + rho

    # Среднее время ожидания
    Tq = Lq / lam

    # Среднее время пребывания
    Ts = Ls / lam

    # Функция затрат
    C = (k / lam) + alpha * Ts

    return {
        "k": k,
        "p0": p0,
        "P_queue": p_queue,
        "Lq": Lq,
        "Ls": Ls,
        "Tq": Tq,
        "Ts": Ts,
        "Cost": C
    }

# Расчет характеристик
results = []

for k in range(k_min, 8):

    results.append(calc_characteristics(k))

# Таблица результатов
df = pd.DataFrame(results)

print("\nТаблица результатов:")
print(df)

# Оптимальное число каналов
best = df.loc[df["Cost"].idxmin()]

k_opt = int(best["k"])

print("\nОптимальное число каналов:")
print(f"k_opt = {k_opt}")


# Для k_min = 1 используем геометрическое распределение

prob = 0

for i in range(n_limit + 2):

    pi = (1 - rho) * (rho ** i)

    prob += pi

print("\nВероятность того,")
print(f"что в очереди не более {n_limit} заявок:")

print(f"P = {prob:.5f}")

# Графики

plt.figure(figsize=(10, 5))

# График функции затрат
plt.plot(df["k"],
         df["Cost"],
         marker='o')
plt.title("Функция затрат")
plt.xlabel("Количество каналов")
plt.ylabel("C(k)")
plt.grid(True)
plt.show()

# ============================================

plt.figure(figsize=(10, 5))

# Среднее время пребывания
plt.plot(df["k"],
         df["Ts"],
         marker='o')
plt.title("Среднее время пребывания в системе")
plt.xlabel("Количество каналов")
plt.ylabel("Tсист")
plt.grid(True)
plt.show()

# ============================================

plt.figure(figsize=(10, 5))

# Средняя длина очереди
plt.plot(df["k"],
         df["Lq"],
         marker='o')
plt.title("Среднее число заявок в очереди")
plt.xlabel("Количество каналов")
plt.ylabel("Lоч")
plt.grid(True)
plt.show()