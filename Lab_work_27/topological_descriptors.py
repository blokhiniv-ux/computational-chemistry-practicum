from rdkit import Chem
from rdkit.Chem import Descriptors

molecules = {
    "Аспирин": "CC(=O)Oc1ccccc1C(=O)O",
    "Парацетамол": "CC(=O)Nc1ccc(O)cc1",
    "Ибупрофен": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "Кофеин": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "Глюкоза": "C(C1C(C(C(C(O1)O)O)O)O)O"
}

descriptor_functions = {
    "RingCount": Descriptors.RingCount,
    "RotatableBonds": Descriptors.NumRotatableBonds,
    "Chi0": Descriptors.Chi0,
    "Chi1": Descriptors.Chi1,
    "Kappa1": Descriptors.Kappa1,
    "Kappa2": Descriptors.Kappa2,
    "Kappa3": Descriptors.Kappa3
}

for name, smiles in molecules.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        continue

    print(f"\n{name}")
    for descriptor_name, function in descriptor_functions.items():
        value = function(mol)
        print(f"{descriptor_name:>18}: {value:.3f}")