import pandas as pd
import numpy as np

df = pd.read_csv("raw_data.csv")

print("Исходное число записей:", len(df))

# Проверка наличия необходимых столбцов
required = [
    "canonical_smiles",
    "standard_value",
    "standard_units",
    "standard_relation",
    "standard_type"
]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"В наборе отсутствуют столбцы: {missing}")


# 1. Оставляем только записи IC50
df = df[df["standard_type"] == "IC50"].copy()
print("После отбора IC50:", len(df))


# 2. Оставляем записи с точным численным значением
df["standard_relation"] = df["standard_relation"].fillna("")

df = df[df["standard_relation"] == "="].copy()
print("После отбора точных значений:", len(df))


# 3. Удаляем записи без химической структуры
df = df.dropna(subset=["canonical_smiles"])
print("После удаления пустых SMILES:", len(df))


# 4. Преобразуем значения активности в числовой формат
df["standard_value"] = pd.to_numeric(
    df["standard_value"],
    errors="coerce"
)

df = df.dropna(subset=["standard_value"])
df = df[df["standard_value"] > 0].copy()

print("После проверки числовых значений:", len(df))


# 5. Приводим значения к нМ
conversion = {
    "nM": 1,
    "uM": 1000,
    "µM": 1000,
    "mM": 1_000_000,
    "M": 1_000_000_000
}

df["standard_units"] = df["standard_units"].astype(str)

df["conversion_factor"] = df["standard_units"].map(conversion)

df = df.dropna(subset=["conversion_factor"]).copy()

df["IC50_nM"] = (
    df["standard_value"] * df["conversion_factor"]
)

df = df[df["IC50_nM"] > 0].copy()

print("После приведения единиц:", len(df))


# 6. Сохранение очищенного набора
df.to_csv("cleaned_data.csv", index=False)

print("\nОчищенные данные сохранены в cleaned_data.csv")