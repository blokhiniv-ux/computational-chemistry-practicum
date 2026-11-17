import pubchempy as pcp
import re

def smart_search():
    print("=== Умный поиск в PubChem ===")
    query = input("Введите название, CAS, SMILES или InChI: ").strip()
    
    if not query:
        print("Вы ничего не ввели.")
        return

    # Угадываем тип запроса
    if query.startswith('InChI='):
        namespace = 'inchi'
        print("🔍 Похоже на InChI...")
    elif re.match(r'^\d{2,7}-\d{2}-\d$', query):
        namespace = 'name' # CAS ищем как name
        print("🔍 Похоже на CAS-номер...")
    elif ' ' not in query and any(char in query for char in ['C', 'c', 'N', 'O', '=', '#', '(', ')']):
        namespace = 'smiles'
        print("🔍 Похоже на SMILES...")
    else:
        namespace = 'name'
        print("🔍 Ищем по названию...")

    try:
        compounds = pcp.get_compounds(query, namespace)
        
        if not compounds:
            print("❌ Ничего не найдено.")
            return
            
        compound = compounds[0]
        print(f"\n✅ Найдено: {compound.iupac_name}")
        print(f"Формула: {compound.molecular_formula}")
        print(f"Масса: {compound.molecular_weight}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    smart_search()