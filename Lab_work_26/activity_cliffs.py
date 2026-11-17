import pandas as pd

from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, DataStructs

df = pd.read_csv("activity_checked.csv")

df = df.dropna(
    subset=["standardized_smiles", "pIC50"]
).reset_index(drop=True)

# Генератор Morgan fingerprints
morgan_gen = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048
)

# Генерация отпечатков
fps = []

for smiles in df["standardized_smiles"]:

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        fps.append(None)
    else:
        fps.append(morgan_gen.GetFingerprint(mol))


# Поиск структурно близких пар
cliffs = []

n = len(df)

for i in range(n):

    if fps[i] is None:
        continue

    similarities = DataStructs.BulkTanimotoSimilarity(
        fps[i],
        fps[i + 1:]
    )

    for offset, similarity in enumerate(similarities):

        j = i + 1 + offset

        if fps[j] is None:
            continue

        activity_difference = abs(
            df.loc[i, "pIC50"] -
            df.loc[j, "pIC50"]
        )

        if similarity > 0.85 and activity_difference > 2:

            cliffs.append({
                "smiles_1": df.loc[i, "standardized_smiles"],
                "smiles_2": df.loc[j, "standardized_smiles"],
                "similarity": round(similarity, 4),
                "pIC50_1": round(df.loc[i, "pIC50"], 2),
                "pIC50_2": round(df.loc[j, "pIC50"], 2),
                "pIC50_difference": round(
                    activity_difference, 2
                )
            })


cliffs_df = pd.DataFrame(cliffs)

cliffs_df.to_csv(
    "activity_cliffs.csv",
    index=False
)

print("Найдено потенциальных activity cliffs:", len(cliffs_df))

print("Результаты сохранены в activity_cliffs.csv")