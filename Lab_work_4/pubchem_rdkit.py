import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

# Получение SMILES из PubChem
compound = pcp.get_compounds('aspirin', 'name')[0]
smiles = compound.connectivity_smiles

# Создание молекулы в RDKit
mol = Chem.MolFromSmiles(smiles)

# Расчёт дескрипторов
print(f"SMILES: {smiles}")
print(f"Молекулярная масса (RDKit): {Descriptors.MolWt(mol):.2f}")
print(f"LogP (RDKit): {Descriptors.MolLogP(mol):.2f}")
print(f"Доноры H-связей: {Lipinski.NumHDonors(mol)}")
print(f"Акцепторы H-связей: {Lipinski.NumHAcceptors(mol)}")

# Проверка правила пяти Липински
mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)
hbd = Lipinski.NumHDonors(mol)
hba = Lipinski.NumHAcceptors(mol)

violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
print(f"\nНарушений правила пяти: {violations}")