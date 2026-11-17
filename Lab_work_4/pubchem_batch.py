import pubchempy as pcp
import pandas as pd

# Список соединений
compounds = ['aspirin', 'caffeine', 'ibuprofen', 'paracetamol', 'glucose']

# Сбор данных
data = []
for name in compounds:
    try:
        compound = pcp.get_compounds(name, 'name')[0]
        data.append({
            'name': name,
            'formula': compound.molecular_formula,
            'mw': compound.molecular_weight,
            'smiles': compound.connectivity_smiles,
            'xlogp': compound.xlogp,
            'tpsa': compound.tpsa
        })
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {e}")

# Сохранение в CSV
df = pd.DataFrame(data)
df.to_csv('compounds.csv', index=False)
print(f"\nСохранено {len(df)} соединений в compounds.csv")
