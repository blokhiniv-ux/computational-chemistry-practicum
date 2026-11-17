from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import numpy as np
import matplotlib.pyplot as plt

# Список родственных и различных молекул для сравнения сходства
smiles_dict = {
    "Benzene": "C1=CC=CC=C1",
    "Toluene": "CC1=CC=CC=C1",
    "Phenol": "OC1=CC=CC=C1",
    "Ethanol": "CCO",
    "Propanol": "CCCO"
}

names = list(smiles_dict.keys())
mols = [Chem.MolFromSmiles(s) for s in smiles_dict.values()]

# Генерируем структурные фингерпринты (Morgan Fingerprints, радиус 2)
fps = [AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=1024) for m in mols]
num_mols = len(mols)

# Создаем пустую матрицу сходства NumPy
similarity_matrix = np.zeros((num_mols, num_mols))

# Рассчитываем коэффициенты Танимото попарно
for i in range(num_mols):
    for j in range(num_mols):
        similarity_matrix[i, j] = DataStructs.TanimotoSimilarity(fps[i], fps[j])

# Визуализация матрицы сходства химических структур
plt.figure(figsize=(6, 5))
plt.imshow(similarity_matrix, cmap='YlGnBu', vmin=0, vmax=1)
plt.colorbar(label='Коэффициент сходства Танимото')

# Настройка осей координат
plt.xticks(range(num_mols), names, rotation=45)
plt.yticks(range(num_mols), names)
plt.title('Матрица структурного сходства молекул')
plt.tight_layout()
plt.show()