from rdkit import Chem
from rdkit.Chem import Descriptors

# Запрос SMILES у пользователя
smiles = input("Введите SMILES-строку соединения: ")

# Создание молекулы из SMILES
mol = Chem.MolFromSmiles(smiles)

# Проверка корректности SMILES
if mol is None:
    print("Ошибка: неверная SMILES-строка. Проверьте скобки, регистр и валентности.")
else:
    mw = Descriptors.MolWt(mol)
    formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
    print(f"Молекулярная формула: {formula}")
    print(f"Молярная масса: {mw:.2f} г/моль")