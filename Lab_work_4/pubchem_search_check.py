import pubchempy as pcp

def get_compound_info(compound_name):
    try:
        # Пытаемся получить список соединений
        compounds = pcp.get_compounds(compound_name, 'name')
        
        # Проверяем, не пустой ли список (защита от опечаток)
        if not compounds:
            print(f"Ошибка: Соединение '{compound_name}' не найдено в PubChem. Проверьте название.")
            return
        
        compound = compounds[0]
        
        # Извлечение свойств (с безопасным выводом, если свойства нет)
        print(f"Название: {compound.iupac_name}")
        print(f"Молекулярная формула: {compound.molecular_formula}")
        print(f"Молекулярная масса: {compound.molecular_weight}")
        # Используем connectivity_smiles, так как canonical_smiles устарел
        print(f"SMILES: {compound.connectivity_smiles}") 
        print(f"InChI: {compound.inchi}")
        print(f"LogP (XLogP): {compound.xlogp}")
        print(f"TPSA: {compound.tpsa}")
        print(f"Доноры H-связей: {compound.h_bond_donor_count}")
        print(f"Акцепторы H-связей: {compound.h_bond_acceptor_count}")
        
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при работе с PubChem: {e}")

# Тестируем
get_compound_info('aspirin')
# get_compound_info('asprin') # Выведет понятное сообщение об ошибке