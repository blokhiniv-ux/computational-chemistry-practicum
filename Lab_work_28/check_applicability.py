import pandas as pd
import joblib

from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, Lipinski
from rdkit.Chem import rdFingerprintGenerator

# Загрузка обучающей выборки
train = pd.read_csv("train_with_desc.csv")

# Загрузка модели и масштабировщика
model = joblib.load("qsar_model.pkl")
scaler = joblib.load("qsar_scaler.pkl")

features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]

# Проверяемые соединения
new_molecules = {
    "Соединение 1": "CC(=O)Oc1ccc(C=C)cc1",
    "Соединение 2": "CC(=O)Oc1ccc(C=O)cc1",
    "Соединение 3": "CC(=O)Oc1ccc(CO)cc1",
    "Крупное соединение": (
        "CCCCCCCCCCCCCCCCCC(=O)"
        "Oc1ccc(CCCCCCCCCCCCCC)cc1"
    )
}

# Границы дескрипторов в обучающей выборке
bounds = {
    feature: (
        train[feature].min(),
        train[feature].max()
    )
    for feature in features
}

# Генератор отпечатков Morgan
generator = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048
)

# Отпечатки обучающих соединений
train_fps = []
for smiles in train["standardized_smiles"]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        train_fps.append(generator.GetFingerprint(mol))

print("=" * 70)
print("ОЦЕНКА ОБЛАСТИ ПРИМЕНИМОСТИ")
print("=" * 70)


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


for name, smiles in new_molecules.items():
    desc = calculate_descriptors(smiles)
    if desc is None:
        print(f"\n{name}: ошибка SMILES")
        continue

    # 1. Проверка диапазонов
    out_of_bounds = []
    for feat, value in desc.items():
        lo, hi = bounds[feat]
        if value < lo or value > hi:
            out_of_bounds.append(
                f"{feat} ({value:.1f} вне [{lo:.1f}, {hi:.1f}])"
            )

    # 2. Максимальное сходство по Morgan/Tanimoto
    mol = Chem.MolFromSmiles(smiles)
    fp = generator.GetFingerprint(mol)
    similarities = DataStructs.BulkTanimotoSimilarity(
        fp, train_fps
    )
    max_sim = max(similarities) if similarities else 0.0

    # 3. Прогноз
    X_new = pd.DataFrame([desc])[features]
    X_new_scaled = scaler.transform(X_new)
    prediction = model.predict(X_new_scaled)[0]

    print(f"\n{name}")
    print(f"  Прогноз pIC50:         {prediction:.2f}")
    print(f"  Макс. сходство:        {max_sim:.3f}")

    if out_of_bounds:
        print("  Выход за диапазоны:")
        for item in out_of_bounds:
            print(f"    - {item}")
    else:
        print("  Все дескрипторы в диапазонах обучения.")

    if max_sim < 0.4:
        print("  Структурное сходство низкое.")
    else:
        print("  Есть структурно близкие соединения.")