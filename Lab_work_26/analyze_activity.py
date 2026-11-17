import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("aggregated_data.csv")

# Проверка значений
df = df.dropna(subset=["pIC50"]).copy()

print("Число соединений:", len(df))
print("Минимальное pIC50:", df["pIC50"].min())
print("Максимальное pIC50:", df["pIC50"].max())
print("Среднее pIC50:", df["pIC50"].mean())
print("Медиана pIC50:", df["pIC50"].median())
print("Стандартное отклонение:", df["pIC50"].std())

# Квартильный размах
q1 = df["pIC50"].quantile(0.25)
q3 = df["pIC50"].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

# Пометка потенциально необычных значений
df["possible_outlier"] = (
    (df["pIC50"] < lower) |
    (df["pIC50"] > upper)
)

print(
    "Число значений, требующих проверки:",
    df["possible_outlier"].sum()
)

# Сохранение результатов
df.to_csv("activity_checked.csv", index=False)

# Гистограмма
plt.figure(figsize=(8, 5))

plt.hist(
    df["pIC50"],
    bins=30,
    edgecolor="black"
)

plt.xlabel("pIC50")
plt.ylabel("Число соединений")
plt.title("Распределение ингибирующей активности")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("pIC50_distribution.png", dpi=300)
plt.show()