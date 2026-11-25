import numpy as np
import matplotlib.pyplot as plt

# Настройки шрифтов для книги
import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Times New Roman']

# Параметры спектра этанола (CDCl3, примерно)
ppm = np.linspace(0.5, 4.5, 4000)   # ось спектра
Hz_per_ppm = 400                    # спектрометр 400 МГц
lw = 2.0                            # ширина линии, Гц

def lorentz(x, x0, h):
    return h / (1 + ((x - x0) * Hz_per_ppm / (lw / 2))**2)

def multiplet(center, intens, J=7):
    n = len(intens)
    offsets = (np.arange(n) - (n - 1) / 2) * J / Hz_per_ppm
    coeffs = np.array(intens) / max(intens)
    return sum(lorentz(ppm, center + o, c) for o, c in zip(offsets, coeffs))

# Формирование спектра
spec  = multiplet(1.2, [1, 2, 1])          # CH3 — триплет
spec += multiplet(3.7, [1, 3, 3, 1])       # CH2 — квартет
spec += lorentz(ppm, 2.0, 1.0)             # OH — синглет

# Построение графика
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ppm, spec, color='black', lw=1.5)
ax.invert_xaxis()                   # ось м.д. идёт справа налево
ax.set_xlabel("δ, м.д.", fontsize=14)
ax.set_ylabel("Интенсивность, отн.", fontsize=14)
ax.set_title("ЯМР ¹H этанола (модель)", fontsize=16)

# Интегрирование
areas = [np.trapezoid(spec[(ppm > a) & (ppm < b)], ppm[(ppm > a) & (ppm < b)])
         for a, b in [(0.8, 1.6), (1.7, 2.3), (3.2, 4.2)]]

norm = np.array(areas) / min(areas)
print("Интегралы (CH3 : OH : CH2):", norm.round(2))

# Сохраняем рисунок в векторный SVG для книги
plt.savefig('ethanol_nmr.svg', format='svg', bbox_inches='tight')
print("Рисунок сохранен в файл ethanol_nmr.svg")

# Показываем окно (после этого программу нужно просто закрыть)
plt.show()
