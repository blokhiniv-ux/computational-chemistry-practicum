import cclib

# Чтение трёх выходных файлов
neutral = cclib.io.ccread("neutral.log")
cation = cclib.io.ccread("cation.log")
anion = cclib.io.ccread("anion.log")

# Извлечение зарядов NPA (если cclib поддерживает)
# Примечание: поддержка NBO в cclib может быть ограничена,
# здесь используем заряды Малликена как пример
q_neutral = neutral.atomcharges['mulliken']
q_cation = cation.atomcharges['mulliken']
q_anion = anion.atomcharges['mulliken']

# Расчёт конденсированных функций Фукуи
n_atoms = len(q_neutral)

print(f"{'Атом':<6} {'f+':<10} {'f-':<10}")
print("-" * 26)

for i in range(n_atoms):
    f_plus = q_neutral[i] - q_anion[i]   # нуклеофильная атака
    f_minus = q_cation[i] - q_neutral[i]  # электрофильная атака
    print(f"{i+1:<6} {f_plus:<10.4f} {f_minus:<10.4f}")

# Поиск атомов с максимальными f+ и f-
max_f_plus = max(range(n_atoms), key=lambda i: q_neutral[i] - q_anion[i])
max_f_minus = max(range(n_atoms), key=lambda i: q_cation[i] - q_neutral[i])

print(f"\nНаиболее электрофильный атом: {max_f_plus + 1} (f+ = {q_neutral[max_f_plus] - q_anion[max_f_plus]:.4f})")
print(f"Наиболее нуклеофильный атом: {max_f_minus + 1} (f- = {q_cation[max_f_minus] - q_neutral[max_f_minus]:.4f})")