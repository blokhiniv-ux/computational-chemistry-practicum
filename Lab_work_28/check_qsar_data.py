import pandas as pd

train = pd.read_csv("train_with_desc.csv")
test = pd.read_csv("test_with_desc.csv")

features = [
    "MW", "LogP", "HBD", "HBA",
    "TPSA", "RotB", "Rings"
]
required_columns = ["standardized_smiles", "pIC50"] + features


def check_dataset(df, name):
    print(f"\n{name}")
    print("-" * 50)

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]
    if missing:
        raise ValueError(
            f"Отсутствуют обязательные столбцы: {missing}"
        )

    print("Количество записей:", len(df))
    print(
        "Количество пропусков:",
        df[required_columns].isna().sum().sum()
    )
    print(
        "Количество повторяющихся SMILES:",
        df["standardized_smiles"].duplicated().sum()
    )

    print("\nРаспределение pIC50:")
    print(df["pIC50"].describe())

    print("\nПервые пять строк:")
    print(df[required_columns].head())


check_dataset(train, "ОБУЧАЮЩАЯ ВЫБОРКА")
check_dataset(test, "ТЕСТОВАЯ ВЫБОРКА")