import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

DESCRIPTOR_NAMES = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]


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


def process_dataset(input_file, output_file):
    df = pd.read_csv(input_file)

    if "standardized_smiles" not in df.columns:
        raise ValueError(
            f"В файле {input_file} отсутствует столбец "
            f"'standardized_smiles'."
        )

    descriptors = []
    for smiles in df["standardized_smiles"]:
        descriptors.append(calculate_descriptors(smiles))

    desc_df = pd.DataFrame(descriptors)
    result = pd.concat(
        [df.reset_index(drop=True), desc_df],
        axis=1
    )

    # Исключаем записи, для которых дескрипторы
    # не удалось рассчитать
    before = len(result)
    result = result.dropna(subset=DESCRIPTOR_NAMES).copy()
    after = len(result)
    if before != after:
        print(
            f"Исключено записей с некорректными структурами: "
            f"{before - after}"
        )

    result.to_csv(output_file, index=False)
    print(f"Сохранено: {output_file} ({len(result)} записей)")


process_dataset("train.csv", "train_with_desc.csv")
process_dataset("test.csv", "test_with_desc.csv")