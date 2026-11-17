# Взять последнюю SCF-энергию (финальную)
final_energy = float(scf[-1]) if scf else None

# Разбить строку частот на отдельные числа
freq_list = []
for line in freqs:
    for value in line.split():
        try:
            freq_list.append(float(value))
        except ValueError:
            pass

# Проверить наличие мнимых частот
n_imaginary = sum(1 for f in freq_list if f < 0)
print(f"Мнимых частот: {n_imaginary}")

if n_imaginary == 0:
    print("Структура — истинный минимум")
elif n_imaginary == 1:
    print("Структура — переходное состояние")
else:
    print("Структура — седловая точка высшего порядка")