import pandas as pd
import numpy as np

df = pd.read_csv("standardized_data.csv")

df["pIC50"] = 9 - np.log10(df["IC50_nM"])

# Агрегирование повторных измерений
aggregated = (
    df.groupby("standardized_smiles")
    .agg(
        pIC50=("pIC50", "median"),
        n_measurements=("pIC50", "count"),
        min_pIC50=("pIC50", "min"),
        max_pIC50=("pIC50", "max"),
        std_pIC50=("pIC50", "std")
    )
    .reset_index()
)

aggregated["range_pIC50"] = (
    aggregated["max_pIC50"] - aggregated["min_pIC50"]
)

aggregated.to_csv("aggregated_data.csv", index=False)

print("Число уникальных соединений:", len(aggregated))
print("Файл сохранён: aggregated_data.csv")