import sqlite3
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

DB_NAME = "chemical_database.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS compounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL COLLATE NOCASE UNIQUE,
            smiles TEXT NOT NULL,
            molecular_weight REAL NOT NULL,
            formula TEXT NOT NULL,
            logp REAL NOT NULL,
            tpsa REAL NOT NULL,
            heavy_atom_count INTEGER NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def calculate_properties(smiles):
    """Проверяет SMILES и возвращает молекулу и набор дескрипторов."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Не удалось разобрать SMILES. Проверьте строку.")

    return {
        "smiles": Chem.MolToSmiles(mol, isomericSmiles=True),
        "molecular_weight": float(Descriptors.MolWt(mol)),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "logp": float(Descriptors.MolLogP(mol)),
        "tpsa": float(Descriptors.TPSA(mol)),
        "heavy_atom_count": int(mol.GetNumHeavyAtoms()),
    }

def add_compound(conn, name, smiles):
    name = name.strip()
    if not name:
        raise ValueError("Введите название соединения.")

    props = calculate_properties(smiles)
    try:
        conn.execute("""
            INSERT INTO compounds
            (name, smiles, molecular_weight, formula, logp, tpsa, heavy_atom_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name, props["smiles"], props["molecular_weight"], props["formula"],
            props["logp"], props["tpsa"], props["heavy_atom_count"]
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Соединение с таким названием уже есть в базе.")

    return props