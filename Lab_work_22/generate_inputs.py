from rdkit import Chem
from rdkit.Chem import AllChem
import os

# Список молекул (SMILES)
molecules = {
    'water': 'O',
    'methanol': 'CO',
    'ethanol': 'CCO',
    'formaldehyde': 'C=O',
    'acetone': 'CC(=O)C',
    'benzene': 'c1ccccc1',
    'phenol': 'Oc1ccccc1',
    'aniline': 'Nc1ccccc1',
    'acetic_acid': 'CC(=O)O',
    'acetaldehyde': 'CC=O'
}

# Создаём папку для входных файлов
os.makedirs('gaussian_inputs', exist_ok=True)

# Генерация входных файлов
for name, smiles in molecules.items():
    # Создание молекулы из SMILES
    mol = Chem.MolFromSmiles(smiles)
    
    # Добавление водородов
    mol = Chem.AddHs(mol)
    
    # Генерация 3D-координат
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)
    
    # Получение координат
    conf = mol.GetConformer()
    coords = []
    for i, atom in enumerate(mol.GetAtoms()):
        pos = conf.GetAtomPosition(i)
        coords.append(f"{atom.GetSymbol():<2} {pos.x:>12.6f} {pos.y:>12.6f} {pos.z:>12.6f}")
    
    # Создание входного файла
    gjf_content = f"""#P B3LYP/6-31G(d) Opt Freq

{name} optimization and frequency

0 1
""" + "\n".join(coords) + "\n"
    
    # Сохранение файла
    with open(f'gaussian_inputs/{name}.gjf', 'w') as f:
        f.write(gjf_content)
    
    print(f"✓ Создан файл: {name}.gjf")

print(f"\nВсего создано файлов: {len(molecules)}")