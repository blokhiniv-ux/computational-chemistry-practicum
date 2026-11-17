"""
Пакетный запуск расчётов Gaussian для всех .gjf-файлов из папки gaussian_inputs.

ВАЖНО: путь к исполняемому файлу должен указывать на КОНСОЛЬНЫЙ g09.exe / g16.exe,
а НЕ на графический g09w.exe / g16w.exe. Графическая оболочка не пишет результаты
в stdout, поэтому .log останется пустым.

Как выбрать версию:
  - Для Gaussian 09: оставьте активной пару строк GAUSSIAN_09_* и закомментируйте GAUSSIAN_16_*.
  - Для Gaussian 16: закомментируйте GAUSSIAN_09_* (поставьте # перед строками)
    и уберите # перед GAUSSIAN_16_*.
"""

import os
import glob
import time
import subprocess


# ============================================================================
#  ВЫБЕРИТЕ ВЕРСИЮ GAUSSIAN — РАСКОММЕНТИРУЙТЕ НУЖНУЮ ПАРУ СТРОК
# ============================================================================

# --- Вариант 1: Gaussian 09 (активен по умолчанию) --------------------------
GAUSSIAN_EXE = r'C:\G09W\g09.exe'
GAUSSIAN_DIR = r'C:\G09W'

# --- Вариант 2: Gaussian 16 -------------------------------------------------
# GAUSSIAN_EXE = r'C:\G16W\g16.exe'
# GAUSSIAN_DIR = r'C:\G16W'

# ============================================================================


INPUT_DIR  = 'gaussian_inputs'
OUTPUT_DIR = 'gaussian_outputs'
TIMEOUT    = 3600          # секунд на один расчёт

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Проверяем, что файл Gaussian действительно существует
if not os.path.isfile(GAUSSIAN_EXE):
    raise SystemExit(
        f"Не найден исполняемый файл Gaussian: {GAUSSIAN_EXE}\n"
        f"Проверьте путь и убедитесь, что это g09.exe / g16.exe "
        f"(а не g09w.exe / g16w.exe)."
    )

# GAUSS_EXEDIR нужен, чтобы g09.exe / g16.exe нашли свои модули (l1.exe и т.д.)
env = os.environ.copy()
env['GAUSS_EXEDIR'] = GAUSSIAN_DIR

gjf_files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.gjf')))

print(f"Используется Gaussian: {GAUSSIAN_EXE}")
print(f"GAUSS_EXEDIR = {GAUSSIAN_DIR}")
print(f"Найдено файлов: {len(gjf_files)}")
print("Расчёты будут выполняться ПОСЛЕДОВАТЕЛЬНО:")
print("  каждый следующий стартует после завершения предыдущего\n")

if not gjf_files:
    raise SystemExit(f"В папке '{INPUT_DIR}' нет ни одного .gjf-файла.")

# ----------------------------------------------------------------------------
#  Последовательный запуск расчётов
# ----------------------------------------------------------------------------
for i, gjf_file in enumerate(gjf_files, 1):
    base_name   = os.path.splitext(os.path.basename(gjf_file))[0]
    output_file = os.path.join(OUTPUT_DIR, f'{base_name}.log')

    print(f"[{i}/{len(gjf_files)}] Запуск расчёта: {base_name}")

    start_time = time.time()

    try:
        with open(output_file, 'w') as f_out:
            # Popen вместо run — чтобы можно было корректно прервать Ctrl+C
            proc = subprocess.Popen(
                [GAUSSIAN_EXE, gjf_file],
                stdout=f_out,
                stderr=subprocess.PIPE,
                env=env,
            )

            try:
                _, stderr_bytes = proc.communicate(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                print(f"    ✗ Превышено время расчёта ({TIMEOUT} сек), завершаю процесс")
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                continue

        elapsed = time.time() - start_time

        if proc.returncode == 0:
            print(f"    ✓ Завершён за {elapsed:.1f} сек → {output_file}")
        else:
            err = (stderr_bytes or b'').decode(errors='replace')
            print(f"    ✗ Ошибка (код {proc.returncode}): {err.strip()}")
            print(f"      Подробности см. в {output_file}")

    except KeyboardInterrupt:
        # Ctrl+C — завершаем текущий Gaussian и выходим из скрипта
        print("\n\nПрервано пользователем, завершаю Gaussian...")
        try:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
        except Exception:
            pass
        print("Остановлено.")
        raise SystemExit(1)

    except FileNotFoundError:
        print(f"    ✗ Gaussian не найден. Проверьте путь: {GAUSSIAN_EXE}")
        break

print("\nВсе расчёты завершены.")