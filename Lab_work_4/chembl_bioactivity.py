from chembl_webresource_client.new_client import new_client

# Получение клиентов API
molecule = new_client.molecule
activity = new_client.activity

# Поиск аспирина в ChEMBL
aspirin = molecule.filter(pref_name__icontains='aspirin')[0]
print(f"ChEMBL ID: {aspirin['molecule_chembl_id']}")
print(f"Название: {aspirin['pref_name']}")

# Получение данных о биологической активности
activities = activity.filter(
    molecule_chembl_id=aspirin['molecule_chembl_id'],
    pchembl_value__isnull=False
).only(['target_pref_name', 'standard_type', 'standard_value', 'standard_units'])

# Вывод первых 10 записей
print("\nБиологическая активность:")
for i, act in enumerate(activities[:10]):
    print(f"{i+1}. Target: {act['target_pref_name']}")
    print(f"   {act['standard_type']}: {act['standard_value']} {act['standard_units']}")