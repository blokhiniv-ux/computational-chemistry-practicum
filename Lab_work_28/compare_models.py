import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

train = pd.read_csv("train_with_desc.csv")
test = pd.read_csv("test_with_desc.csv")

features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]

X_train = train[features]
y_train = train["pIC50"]
X_test = test[features]
y_test = test["pIC50"]

# Линейная регрессия
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)

# Случайный лес (без масштабирования)
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Сравнение метрик
def report(name, y_true, y_pred):
    print(f"\n{name}")
    print(f"  R²:   {r2_score(y_true, y_pred):.3f}")
    print(
        f"  RMSE: "
        f"{np.sqrt(mean_squared_error(y_true, y_pred)):.3f}"
    )
    print(
        f"  MAE:  "
        f"{mean_absolute_error(y_true, y_pred):.3f}"
    )

report("Линейная регрессия", y_test, y_pred_lr)
report("Случайный лес", y_test, y_pred_rf)

# Важность дескрипторов (для случайного леса)
print("\nВажность дескрипторов (Random Forest):")
importances = rf_model.feature_importances_
order = np.argsort(importances)[::-1]
for idx in order:
    print(f"  {features[idx]:>6}: {importances[idx]:.3f}")

plt.figure(figsize=(8, 5))
plt.bar(
    [features[i] for i in order],
    importances[order],
    color="seagreen"
)
plt.ylabel("Относительная важность")
plt.title("Важность дескрипторов (Random Forest)")
plt.tight_layout()
plt.savefig("rf_importances.png", dpi=150)
plt.show()