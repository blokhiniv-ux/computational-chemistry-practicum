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
    f"{'Молекула':<15} {'MW':<8} {'LogP':<8} "
    f"{'HBD':<5} {'HBA':<5} {'Нарушений':<12}"
)
print("-" * 65)

for name, smiles in molecules.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        continue

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)

    violations = 0
    if mw > 500:
        violations += 1
    if logp > 5:
        violations += 1
    if hbd > 5:
        violations += 1
    if hba > 10:
        violations += 1

    print(
        f"{name:<15} {mw:<8.1f} {logp:<8.2f} "
        f"{hbd:<5} {hba:<5} {violations:<12}"
    )