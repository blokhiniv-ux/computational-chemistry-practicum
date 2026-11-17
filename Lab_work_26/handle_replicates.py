import pandas as pd

df = pd.read_csv("standardized_data.csv")

# Число экспериментальных измерений для каждой структуры
counts = (
    df.groupby("standardized_smiles")
    .size()
    .sort_values(ascending=False)
)

print("Число уникальных структур:", len(counts))
print("Структур с несколькими измерениями:", (counts > 1).sum())

# Оценка разброса pIC50 будет проведена после логарифмирования
import numpy as np

df["pIC50"] = 9 - np.log10(df["IC50_nM"])

# Описательная статистика для каждой структуры
summary = (
    df.groupby("standardized_smiles")
    .agg(
        n_measurements=("pIC50", "count"),
        median_pIC50=("pIC50", "median"),
        mean_pIC50=("pIC50", "mean"),
        min_pIC50=("pIC50", "min"),
        max_pIC50=("pIC50", "max"),
        std_pIC50=("pIC50", "std")
    )
    .reset_index()
)

summary["range_pIC50"] = (
    summary["max_pIC50"] - summary["min_pIC50"]
)

summary.to_csv("replicate_summary.csv", index=False)

print("\nСтатистика повторных измерений сохранена.")