import pandas as pd

from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

from sklearn.model_selection import GroupShuffleSplit

df = pd.read_csv("activity_checked.csv")

# Удаляем записи без необходимых данных
df = df.dropna(
    subset=["standardized_smiles", "pIC50"]
).copy()


# Функция получения каркаса Bemis-Murcko
def get_scaffold(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    scaffold = MurckoScaffold.GetScaffoldForMol(mol)

    if scaffold is None or scaffold.GetNumAtoms() == 0:
        return "ACYCLIC_" + smiles

    return Chem.MolToSmiles(
        scaffold,
        canonical=True
    )


df["scaffold"] = (
    df["standardized_smiles"].apply(get_scaffold)
)

df = df.dropna(subset=["scaffold"]).copy()

print("Число соединений:", len(df))
print("Число уникальных каркасов:", df["scaffold"].nunique())


# Разделение по структурным каркасам
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(
        df,
        groups=df["scaffold"]
    )
)

train = df.iloc[train_idx].copy()
test = df.iloc[test_idx].copy()


# Проверка отсутствия общих каркасов
common_scaffolds = (
    set(train["scaffold"]) &
    set(test["scaffold"])
)

print("Общие каркасы:", len(common_scaffolds))

if common_scaffolds:
    raise ValueError(
        "Обнаружены общие каркасы в обучающей и тестовой выборках."
    )


train.to_csv("train.csv", index=False)
test.to_csv("test.csv", index=False)

print("\nОбучающая выборка:", len(train))
print("Тестовая выборка:", len(test))

print(
    "Среднее pIC50 (обучение):",
    round(train["pIC50"].mean(), 2)
)

print(
    "Среднее pIC50 (тест):",
    round(test["pIC50"].mean(), 2)
)

print("\nФайлы train.csv и test.csv сохранены.")