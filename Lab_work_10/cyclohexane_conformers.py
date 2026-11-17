"""
Поиск конформеров циклогексана с помощью RDKit (ETKDGv3).

Алгоритм:
  1. Молекула из SMILES + явные атомы H.
  2. Генерация N стартовых конформеров методом ETKDGv3
     (с учётом стереохимии малых колец — useSmallRingTorsions).
  3. Оптимизация геометрии в силовом поле MMFF94.
  4. Кластеризация по RMSD: из близких по форме структур остаётся одна.
  5. Сохранение в отдельные .mol-файлы (HyperChem открывает с готовыми связями)
     и общий .sdf со всеми конформерами.

Запуск:
    python cyclohexane_conformers.py
"""

import os
from rdkit import Chem
from rdkit.Chem import AllChem, rdDistGeom, rdBase

# ----------------------------- настройки ------------------------------------
SMILES            = "C1CCCCC1"          # циклогексан
NUM_CONFS         = 200                 # сколько стартовых структур сгенерировать
RANDOM_SEED       = 0xC0FFEE            # для воспроизводимости
ENERGY_WINDOW     = 10.0                # ккал/моль — окно, в котором ищем конформеры
                                        # (у циклогексана chair→boat ≈ 7 ккал/моль)
RMS_THRESH        = 0.5                 # Å — структуры ближе этого считаем одинаковыми
OUT_DIR           = "cyclohexane_conformers"
MMFF_VARIANT      = "MMFF94"
# ----------------------------------------------------------------------------

print(f"RDKit {rdBase.rdkitVersion}")

# 1. Молекула с явными водородами
mol = Chem.MolFromSmiles(SMILES)
if mol is None:
    raise SystemExit(f"Не удалось разобрать SMILES: {SMILES}")
mol = Chem.AddHs(mol)

# 2. Параметры ETKDGv3
params = rdDistGeom.ETKDGv3()
params.randomSeed        = RANDOM_SEED
params.pruneRmsThresh    = -1          # не отбрасывать на этапе встраивания
params.numThreads        = 0           # все доступные потоки
# Важно для колец: без этих флагов ETKDG часто «схлопывает» всё в одну форму
for attr, val in [("useSmallRingTorsions", True),
                  ("useMacrocycleTorsions", True)]:
    if hasattr(params, attr):
        setattr(params, attr, val)

conf_ids = list(rdDistGeom.EmbedMultipleConfs(mol, numConfs=NUM_CONFS, params=params))
print(f"Сгенерировано стартовых конформеров: {len(conf_ids)}")
if not conf_ids:
    raise SystemExit("Встраивание не дало ни одной структуры — увеличьте NUM_CONFS.")

# 3. Оптимизация MMFF94
results = AllChem.MMFFOptimizeMoleculeConfs(
    mol, mmffVariant=MMFF_VARIANT, numThreads=0
)
energies = [(cid, e, nc) for cid, (nc, e) in enumerate(results)]
energies.sort(key=lambda t: t[1])

e_min = energies[0][1]
print(f"\nМинимальная энергия: {e_min:.3f} ккал/моль ({MMFF_VARIANT})")
print(f"{'conf':>6} {'E, ккал/моль':>14} {'ΔE':>8} {'сошлось':>8}")
for cid, e, nc in energies[:15]:
    print(f"{cid:>6} {e:>14.3f} {e - e_min:>8.3f} {'да' if nc == 0 else 'нет':>8}")

# 4. Кластеризация: сначала отбрасываем всё выше ENERGY_WINDOW,
#    затем оставляем по одному представителю из каждой группы близких по RMSD
def cluster(mol, energies, e_min, e_win, rms_thresh):
    kept = [(cid, e) for cid, e, _ in energies if e - e_min <= e_win]
    kept.sort(key=lambda t: t[1])
    selected = []
    for cid, e in kept:
        if all(AllChem.GetBestRMS(mol, mol, prbId=cid, refId=sid) >= rms_thresh
               for sid, _ in selected):
            selected.append((cid, e))
    return selected

unique = cluster(mol, energies, e_min, ENERGY_WINDOW, RMS_THRESH)
print(f"\nУникальных конформеров в окне ΔE ≤ {ENERGY_WINDOW} ккал/моль "
      f"и RMS ≥ {RMS_THRESH} Å: {len(unique)}")
print(f"{'#':>3} {'conf':>6} {'E, ккал/моль':>14} {'ΔE':>8}")
for i, (cid, e) in enumerate(unique, 1):
    print(f"{i:>3} {cid:>6} {e:>14.3f} {e - e_min:>8.3f}")

# 5. Сохранение результатов
os.makedirs(OUT_DIR, exist_ok=True)

# 5a. Один SDF со всеми конформерами — для архива / внешних инструментов
sdf_all = os.path.join(OUT_DIR, "cyclohexane_all.sdf")
writer = Chem.SDWriter(sdf_all)
for cid, e, nc in energies:
    mol.SetProp("_Name", f"conf_{cid:03d}")
    mol.SetProp("MMFF94_energy_kcal_per_mol", f"{e:.4f}")
    mol.SetProp("dE_kcal_per_mol", f"{e - e_min:.4f}")
    writer.write(mol, confId=cid)
writer.close()

# 5b. Отдельные .mol-файлы для уникальных конформеров — для HyperChem
for i, (cid, e) in enumerate(unique, 1):
    stem = f"conf_{i:02d}_E{e - e_min:.2f}"
    with open(os.path.join(OUT_DIR, stem + ".mol"), "w") as f:
        f.write(Chem.MolToMolBlock(mol, confId=cid))
    # дубликат в XYZ — на случай, если нужен простой формат
    with open(os.path.join(OUT_DIR, stem + ".xyz"), "w") as f:
        f.write(Chem.MolToXYZBlock(mol, confId=cid))

print(f"\nФайлы сохранены в папку '{OUT_DIR}/':")
print(f"  {sdf_all}  — все конформеры")
print(f"  conf_XX_E*.*  — по файлу на каждый уникальный конформер")
print("\nДля просмотра в HyperChem откройте нужный .mol-файл (File → Open).")