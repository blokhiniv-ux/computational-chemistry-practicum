import pubchempy as pcp

# Поиск аспирина по названию
compound = pcp.get_compounds('aspirin', 'name')[0]

# Извлечение свойств
print(f"Название: {compound.iupac_name}")
print(f"Молекулярная формула: {compound.molecular_formula}")
print(f"Молекулярная масса: {compound.molecular_weight}")
print(f"SMILES: {compound.connectivity_smiles}")  # Исправлено: вместо canonical_smiles
print(f"InChI: {compound.inchi}")
print(f"LogP (XLogP): {compound.xlogp}")
print(f"TPSA: {compound.tpsa}")
print(f"Доноры H-связей: {compound.h_bond_donor_count}")
print(f"Акцепторы H-связей: {compound.h_bond_acceptor_count}")  # 