import numpy as np
import matplotlib.pyplot as plt

# Параметры спектра этанола (CDCl3, примерно)
# CH3: триплет, d=1.2 м.д., J=7 Гц; CH2: квартет, d=3.7 м.д.; OH: синглет, d=2.0 м.д.
ppm = np.linspace(0.5, 4.5, 4000)   # ось спектра
Hz_per_ppm = 400                    # спектрометр 400 МГц: 1 м.д. = 400 Гц
lw = 2.0                            # ширина линии, Гц

def lorentz(x, x0, h):
    return h / (1 + ((x - x0) * Hz_per_ppm / (lw / 2))**2)

def multiplet(center, intens, J=7):
    """Мультиплет: позиции линий от J, интенсивности по биномиальным коэффициентам"""
    n = len(intens)
    offsets = (np.arange(n) - (n - 1) / 2) * J / Hz_per_ppm
    coeffs = np.array(intens) / max(intens)
    return sum(lorentz(ppm, center + o, c) for o, c in zip(offsets, coeffs))

spec  = multiplet(1.2, [1, 2, 1])          # CH3 — триплет 3H
spec += multiplet(3.7, [1, 3, 3, 1])       # CH2 — квартет 2H
spec += lorentz(ppm, 2.0, 1.0)             # OH — синглет 1H

plt.plot(ppm, spec)
plt.gca().invert_xaxis()                   # в ЯМР ось м.д. идёт справа налево!
plt.xlabel("δ, м.д."); plt.ylabel("Интенсивность, отн.")
plt.title("ЯМР ¹H этанола (модель)")
plt.show()

# Интегрирование — проверяем соотношение 3:2:1
areas = [np.trapz(spec[(ppm > a) & (ppm < b)], ppm[(ppm > a) & (ppm < b)])
         for a, b in [(0.8, 1.6), (3.2, 4.2), (1.7, 2.3)]]
norm = np.array(areas) / min(areas)
print("Интегралы (CH3 : OH : CH2):", norm.round(2))