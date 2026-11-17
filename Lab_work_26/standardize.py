import pandas as pd

from rdkit import Chem
from rdkit.Chem import SaltRemover

df = pd.read_csv("cleaned_data.csv")

remover = SaltRemover.SaltRemover()


def standardize(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            return None

        # Удаление небольших неорганических фрагментов
        mol = remover.StripMol(mol, dontRemoveEverything=True)

        if mol is None or mol.GetNumAtoms() == 0:
            return None

        # Канонизация SMILES
        canonical = Chem.MolToSmiles(
            mol,
            canonical=True
        )

        return canonical

    except Exception:
        return None


df["standardized_smiles"] = (
    df["canonical_smiles"].apply(standardize)
)

before = len(df)

df = df.dropna(subset=["standardized_smiles"]).copy()

after = len(df)

print("Исходное число записей:", before)
print("После стандартизации:", after)
print("Записей с некорректными структурами:", before - after)


# Сохраняем все измерения, даже если структуры повторяются
df.to_csv("standardized_data.csv", index=False)

# Отдельно оцениваем число уникальных структур
unique_structures = df["standardized_smiles"].nunique()

print("Число уникальных структур:", unique_structures)
print("Число повторных структурных записей:", len(df) - unique_structures)