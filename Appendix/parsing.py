import re

with open('water.log') as f:
    log = f.read()

# Извлечь SCF-энергию
scf = re.findall(r'SCF Done:\s+E\([^)]+\)\s+=\s+(-?\d+\.\d+)', log)
print("SCF-энергии:", scf)

# Извлечь частоты
freqs = re.findall(r'Frequencies --\s+([-\d\.\s]+)', log)
print("Частоты:", freqs)

# Проверить, сошлась ли оптимизация
if 'Stationary point found' in log:
    print("Оптимизация сошлась")
else:
    print("Оптимизация НЕ сошлась")