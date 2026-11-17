import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv('results.csv')

# График 1: HOMO/LUMO для разных молекул
fig, ax = plt.subplots(figsize=(12, 6))

x = range(len(df))
width = 0.35

ax.bar([i - width/2 for i in x], df['homo_eV'], width, label='HOMO', color='steelblue')
ax.bar([i + width/2 for i in x], df['lumo_eV'], width, label='LUMO', color='coral')

ax.set_xlabel('Молекула')
ax.set_ylabel('Энергия (эВ)')
ax.set_title('Энергии HOMO и LUMO для серии молекул')
ax.set_xticks(x)
ax.set_xticklabels(df['molecule'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('homo_lumo.png', dpi=150)
plt.show()

# График 2: Энергетическая щель
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(df['molecule'], df['gap_eV'], color='mediumseagreen')
ax.set_xlabel('Молекула')
ax.set_ylabel('Энергетическая щель (эВ)')
ax.set_title('HOMO-LUMO щель для серии молекул')
ax.set_xticklabels(df['molecule'], rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('gap.png', dpi=150)
plt.show()

print("Графики сохранены: homo_lumo.png, gap.png")