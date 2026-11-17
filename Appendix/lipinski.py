from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

# Запрос SMILES у пользователя
smiles = input("Введите SMILES-строку соединения: ")

# Создание молекулы из SMILES
mol = Chem.MolFromSmiles(smiles)

# Проверка корректности SMILES
if mol is None:
    print("Ошибка: неверная SMILES-строка. Проверьте скобки, регистр и валентности.")
else:
    # Расчёт дескрипторов
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    formula = Chem.rdMolDescriptors.CalcMolFormula(mol)

    # Вывод результатов
    print(f"\nСоединение: {formula}")
    print(f"{'Параметр':<25} {'Значение':<10} {'Норма':<10}")
    print("-" * 45)
    print(f"{'Молярная масса':<25} {mw:<10.1f} {'< 500':<10}")
    print(f"{'LogP':<25} {logp:<10.2f} {'< 5':<10}")
    print(f"{'Доноры H-связей':<25} {hbd:<10} {'< 5':<10}")
    print(f"{'Акцепторы H-связей':<25} {hba:<10} {'< 10':<10}")

    # Подсчёт нарушений
    violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
    print(f"\nНарушений: {violations} из 4")

    # Интерпретация
    if violations > 1:
        print("Соединение может плохо всасываться")
    else:
        print("Соединение соответствует правилу пяти")