import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.metrics import r2_score, mean_absolute_error

# Загрузка данных
train = pd.read_csv("train_with_desc.csv")
test = pd.read_csv("test_with_desc.csv")

features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]

# Загрузка модели и масштабировщика
model = joblib.load("qsar_model.pkl")
scaler = joblib.load("qsar_scaler.pkl")

# Подготовка признаков
X_train = train[features]
X_test = test[features]
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Прогноз
y_train = train["pIC50"]
y_test = test["pIC50"]
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Метрики тестовой выборки
r2 = r2_score(y_test, y_test_pred)
mae = mean_absolute_error(y_test, y_test_pred)

# График
plt.figure(figsize=(8, 8))
plt.scatter(
    y_train, y_train_pred,
    color="steelblue",
    label="Обучающая", alpha=0.7
)
plt.scatter(
    y_test, y_test_pred,
    color="coral",
    label="Тестовая", alpha=0.7
)

all_values = list(y_train) + list(y_test) + \
             list(y_train_pred) + list(y_test_pred)
lo = min(all_values) - 0.5
hi = max(all_values) + 0.5
plt.plot([lo, hi], [lo, hi], "k--", label="Идеальный прогноз")

plt.xlabel("Экспериментальный pIC50")
plt.ylabel("Предсказанный pIC50")
plt.title(
    f"QSAR: прогноз vs эксперимент "
    f"(R² = {r2:.2f}, MAE = {mae:.2f})"
)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("qsar_plot.png", dpi=150)
plt.show()