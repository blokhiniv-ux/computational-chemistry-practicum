from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

molecules = {
    "Аспирин": "CC(=O)Oc1ccccc1C(=O)O",
    "Парацетамол": "CC(=O)Nc1ccc(O)cc1",
    "Ибупрофен": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "Кофеин": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "Глюкоза": "C(C1C(C(C(C(O1)O)O)O)O)O"
}

print(
    f"{'Молекула':<15} {'MW':<9} {'LogP':<9} "
    f"{'HBD':<6} {'HBA':<6} {'TPSA':<9} {'RotB':<6}"
)
print("-" * 70)

for name, smiles in molecules.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"{name:<15} Ошибка структуры")
        continue

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    tpsa = Descriptors.TPSA(mol)
    rotb = Descriptors.NumRotatableBonds(mol)

    print(
        f"{name:<15} {mw:<9.1f} {logp:<9.2f} "
        f"{hbd:<6} {hba:<6} {tpsa:<9.2f} {rotb:<6}"
    )