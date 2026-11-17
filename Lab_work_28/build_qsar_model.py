import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

# 1. Загрузка данных
train = pd.read_csv("train_with_desc.csv")
test = pd.read_csv("test_with_desc.csv")

# 2. Выбор признаков
features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]
target = "pIC50"

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# 3. Проверка пропущенных значений
if X_train.isna().any().any():
    raise ValueError("В train есть пропуски в дескрипторах")
if X_test.isna().any().any():
    raise ValueError("В test есть пропуски в дескрипторах")

# 4. Масштабирование (только по обучающей выборке!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Обучение модели
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 6. Прогнозы
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# 7. Метрики
def compute_metrics(y_true, y_pred, label):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    print(f"\n{label}")
    print(f"R²:   {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE:  {mae:.3f}")

compute_metrics(y_train, y_train_pred, "ОБУЧАЮЩАЯ ВЫБОРКА")
compute_metrics(y_test, y_test_pred, "ТЕСТОВАЯ ВЫБОРКА")

# 8. Коэффициенты модели
print("\nКоэффициенты регрессии:")
for name, coef in zip(features, model.coef_):
    print(f"  {name:>6}: {coef:+.4f}")
print(f"  Свободный член: {model.intercept_:.4f}")

# 9. Сохранение модели и масштабировщика
joblib.dump(model, "qsar_model.pkl")
joblib.dump(scaler, "qsar_scaler.pkl")
print("\nМодель сохранена в qsar_model.pkl")
print("Масштабировщик сохранён в qsar_scaler.pkl")