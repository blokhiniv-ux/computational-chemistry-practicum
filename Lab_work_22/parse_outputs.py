import os
import glob
import cclib
import pandas as pd

OUTPUT_DIR = 'gaussian_outputs'

data_list = []

for log_file in sorted(glob.glob(os.path.join(OUTPUT_DIR, '*.log'))):
    # На Windows пути с обратным слэшем — используем basename/splitext,
    # а не split('/'). splitext снимает расширение .log/.LOG/.out и т.д.
    base_name = os.path.splitext(os.path.basename(log_file))[0]

    try:
        data = cclib.io.ccread(log_file)
        if data is None:
            print(f"✗ Не удалось прочитать: {base_name}")
            continue

        # --- HOMO и LUMO (cclib уже отдаёт значения в эВ) ---
        homo_energy = lumo_energy = gap = None
        moenergies = getattr(data, 'moenergies', None)
        homos      = getattr(data, 'homos', None)
        if (moenergies is not None and len(moenergies) > 0
                and homos is not None and len(homos) > 0):
            alpha_mo = moenergies[0]
            homo_idx = int(homos[0])
            if homo_idx < len(alpha_mo):
                homo_energy = float(alpha_mo[homo_idx])
            if homo_idx + 1 < len(alpha_mo):
                lumo_energy = float(alpha_mo[homo_idx + 1])
            if homo_energy is not None and lumo_energy is not None:
                gap = lumo_energy - homo_energy

        # --- Энергия SCF (в эВ) ---
        scfenergies = getattr(data, 'scfenergies', None)
        scf_energy = (float(scfenergies[-1])
                      if scfenergies is not None and len(scfenergies) > 0
                      else None)

        # --- Дипольный момент: сохраняем модуль в дебаях ---
        dipole = None
        dip = getattr(data, 'dipole', None)
        if dip is not None and len(dip) > 0:
            dipole = float((dip ** 2).sum() ** 0.5)

        # --- Число атомов ---
        atomnos = getattr(data, 'atomnos', None)
        n_atoms = int(len(atomnos)) if atomnos is not None else None

        data_list.append({
            'molecule':      base_name,
            'scf_energy_eV': scf_energy,
            'homo_eV':       homo_energy,
            'lumo_eV':       lumo_energy,
            'gap_eV':        gap,
            'dipole_D':      dipole,
            'n_atoms':       n_atoms,
        })
        print(f"✓ Обработан: {base_name}")

    except Exception as e:
        print(f"✗ Ошибка при обработке {base_name}: {e}")

df = pd.DataFrame(data_list)
df.to_csv('results.csv', index=False)

print(f"\nОбработано файлов: {len(data_list)}")
print(f"Результаты сохранены в results.csv")
if not df.empty:
    print("\nПервые 5 строк:")
    print(df.head())
else:
    print("\nDataFrame пуст — проверьте содержимое gaussian_outputs/*.log.")