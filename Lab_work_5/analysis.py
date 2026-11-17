import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("chemical_database.db")
try:
    df = pd.read_sql_query("""
        SELECT name, molecular_weight, logp, tpsa, heavy_atom_count
        FROM compounds
        ORDER BY name
    """, conn)
finally:
    conn.close()

if df.empty:
    raise SystemExit("База пуста. Сначала выполните python init_db.py и добавьте соединения.")

print("=== Число соединений ===")
print(len(df))
print("\n=== Описательная статистика ===")
# Совместимо со старыми версиями pandas: явно берём только числовые столбцы.
# (аргумент numeric_only у DataFrame.describe появился только в pandas 1.3.0)
numeric_df = df.select_dtypes(include="number")
print(numeric_df.describe().round(2))

# Упрощённая учебная проверка двух критериев правила пяти Липински.
violations = df[
    (df["molecular_weight"] > 500) |
    (df["logp"] > 5)
]
print(
    f"\nПрепараты с MW > 500 Да или LogP > 5: "
    f"{len(violations)} из {len(df)}"
)
print(violations[["name", "molecular_weight", "logp"]].to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].hist(df["molecular_weight"], bins=15, edgecolor="black")
axes[0].axvline(500, linestyle="--", label="500 Да")
axes[0].set_title("Распределение молекулярной массы")
axes[0].set_xlabel("Молекулярная масса, Да")
axes[0].set_ylabel("Число соединений")
axes[0].legend()

points = axes[1].scatter(
    df["logp"], df["tpsa"], c=df["molecular_weight"], edgecolors="black"
)
axes[1].set_title("LogP и TPSA")
axes[1].set_xlabel("LogP")
axes[1].set_ylabel("TPSA, Å²")
fig.colorbar(points, ax=axes[1], label="Молекулярная масса, Да")

fig.tight_layout()
fig.savefig("drugs_analysis.png", dpi=160)
print("\nГрафик сохранён в файл drugs_analysis.png")
plt.show()