import matplotlib.pyplot as plt
import numpy as np

# Данные
x = np.linspace(1, 12, 12)  # месяцы
y1 = np.random.uniform(50, 100, 12)  # цены на товар 1
y2 = np.random.uniform(40, 90, 12)   # цены на товар 2
y3 = np.random.uniform(60, 110, 12)  # цены на товар 3

# Построение графика с тёмной темой
plt.style.use("dark_background")
plt.figure(figsize=(8, 5))
plt.plot(x, y1, label="Магазин 1", linewidth=2)
plt.plot(x, y2, label="Магазин 2", linewidth=2)
plt.plot(x, y3, label="Магазин 3", linewidth=2)

plt.xlabel("Месяц")
plt.ylabel("Цена, ₽")
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()
