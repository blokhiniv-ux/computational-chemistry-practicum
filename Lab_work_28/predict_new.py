import pandas as pd
import joblib

from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

# Загрузка модели и масштабировщика
model = joblib.load("qsar_model.pkl")
scaler = joblib.load("qsar_scaler.pkl")

features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]

# Новые соединения.
# SMILES замените на структуры,
# выбранные для вашего исследования.
new_molecules = {
    "Соединение 1": "CC(=O)Oc1ccc(C=C)cc1",
    "Соединение 2": "CC(=O)Oc1ccc(C=O)cc1",
    "Соединение 3": "CC(=O)Oc1ccc(CO)cc1"
}


def calculate_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "MW": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "HBD": Lipinski.NumHDonors(mol),
        "HBA": Lipinski.NumHAcceptors(mol),
        "TPSA": Descriptors.TPSA(mol),
        "RotB": Descriptors.NumRotatableBonds(mol),
        "Rings": Descriptors.RingCount(mol)
    }


print(f"{'Соединение':<20} {'pIC50 прогноз':>14}")
print("-" * 40)

for name, smiles in new_molecules.items():
    desc = calculate_descriptors(smiles)
    if desc is None:
        print(f"{name:<20} Ошибка SMILES")
        continue

    X_new = pd.DataFrame([desc])[features]
    X_new_scaled = scaler.transform(X_new)
    prediction = model.predict(X_new_scaled)[0]
    print(f"{name:<20} {prediction:>14.2f}")