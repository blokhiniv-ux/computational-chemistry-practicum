Анализ готовых log-файлов Gaussian для поиска переходного состояния.
Соответствует заданию 7 (для самых быстрых) лабораторной № 22.

Что делает:
  - читает log-файл (или несколько) через cclib;
  - извлекает энергию SCF, число частот, число мнимых частот, значение
    мнимой частоты (см-1), факт нормального завершения;
  - если известен log-файл реагента, считает энергию активации
    Ea = (E_TS - E_reactant) * 627.509 ккал/моль;
  - если известен log-файл продукта, считает dE реакции;
  - классифицирует TS:
      ok_one_imaginary  — ровно одна мнимая частота (истинное TS),
      no_imaginary      — мнимых нет (структура ушла в минимум),
      N_imaginary       — больше одной мнимой частоты,
      no_freq_calc      — частотный анализ не проводился,
      not_converged     — расчёт не завершился нормально.

Режимы запуска:
  python ts_analyze.py file.log
  python ts_analyze.py file1.log file2.log file3.log
  python ts_analyze.py --reactant r.log --ts ts.log [--product p.log]
  python ts_analyze.py --pairs pairs.csv
  python ts_analyze.py --dir gaussian_outputs

Файл pairs.csv (опционально):
  reaction,reactant,ts,product
  HCN_to_HNC,ts_search/HCN_to_HNC_reactant.log,ts_search/HCN_to_HNC_qst2.log,
  NH3_inversion,ts_search/NH3_inversion_reactant.log,ts_search/NH3_inversion_qst2.log,
  CH3NC_to_CH3CN,ts_search/CH3NC_to_CH3CN_reactant.log,ts_search/CH3NC_to_CH3CN_qst2.log,
"""

import argparse
import os
import sys
import glob

import cclib
import pandas as pd

KCA = 627.509   # Hartree -> kcal/mol


# ---------------------------------------------------------------------------
#  Разбор одного log-файла
# ---------------------------------------------------------------------------
def analyze_log(log_path):
    """Возвращает словарь с ключевыми величинами из одного log-файла."""
    res = {
        'file':                 os.path.basename(log_path),
        'path':                 log_path,
        'normal_termination':   None,
        'E_Ha':                 None,
        'n_atoms':              None,
        'n_freqs':              None,
        'n_imag':               None,
        'imag_freq_cm-1':       None,
        'error':                None,
    }

    if not os.path.isfile(log_path):
        res['error'] = 'file not found'
        return res

    try:
        data = cclib.io.ccread(log_path)
    except Exception as e:
        res['error'] = f'cclib error: {e}'
        return res

    if data is None:
        res['error'] = 'cclib returned None (unrecognized format?)'
        return res

    metadata = getattr(data, 'metadata', {}) or {}
    res['normal_termination'] = bool(metadata.get('success', False))

    # Энергия SCF (последняя итерация)
    scf = getattr(data, 'scfenergies', None)
    if scf is not None and len(scf) > 0:
        res['E_Ha'] = float(scf[-1])

    # Число атомов
    atomnos = getattr(data, 'atomnos', None)
    if atomnos is not None:
        res['n_atoms'] = int(len(atomnos))

    # Частоты (cclib отдаёт мнимые как отрицательные числа, см-1)
    freqs = getattr(data, 'vibfreqs', None)
    if freqs is not None and len(freqs) > 0:
        freqs = list(freqs)
        imaginary = sorted(f for f in freqs if f < 0)
        res['n_freqs'] = len(freqs)
        res['n_imag']  = len(imaginary)
        if imaginary:
            res['imag_freq_cm-1'] = round(imaginary[0], 2)

    return res


def classify_ts(ts_res):
    """Классификация по числу мнимых частот."""
    if not ts_res['normal_termination']:
        return 'not_converged'
    if ts_res['n_imag'] is None:
        return 'no_freq_calc'
    if ts_res['n_imag'] == 1:
        return 'ok_one_imaginary'
    if ts_res['n_imag'] == 0:
        return 'no_imaginary'
    return f'{ts_res["n_imag"]}_imaginary'


# ---------------------------------------------------------------------------
#  Расчёт Ea и dE для одной реакции
# ---------------------------------------------------------------------------
def analyze_reaction(name, reactant_path, ts_path, product_path=None):
    r = analyze_log(reactant_path)
    t = analyze_log(ts_path)
    p = analyze_log(product_path) if product_path else None

    Ea = None
    if r['E_Ha'] is not None and t['E_Ha'] is not None:
        Ea = (t['E_Ha'] - r['E_Ha']) * KCA

    dE = None
    if (r['E_Ha'] is not None and p is not None
            and p['E_Ha'] is not None):
        dE = (p['E_Ha'] - r['E_Ha']) * KCA

    status = classify_ts(t)

    common = {
        'reaction':          name,
        'status_ts':         status,
        'Ea_kcal':           round(Ea, 2) if Ea is not None else None,
        'dE_reaction_kcal':  round(dE, 2) if dE is not None else None,
    }

    def make_row(role, res):
        row = dict(common)
        row['role'] = role
        row.update({k: v for k, v in res.items() if k not in ('path', 'error')})
        if res['error']:
            row['error'] = res['error']
        return row

    rows = [make_row('reactant', r), make_row('ts', t)]
    if p is not None:
        rows.append(make_row('product', p))
    return rows


# ---------------------------------------------------------------------------
#  Сбор всех строк таблицы
# ---------------------------------------------------------------------------
def collect_rows(args):
    rows = []

    # Режим 1: одна пара (реагент + TS, опционально продукт)
    if args.reactant and args.ts:
        rows.extend(analyze_reaction(
            name=args.name or 'reaction',
            reactant_path=args.reactant,
            ts_path=args.ts,
            product_path=args.product,
        ))

    # Режим 2: список пар в CSV
    elif args.pairs:
        pairs_df = pd.read_csv(args.pairs)
        required = {'reactant', 'ts'}
        if not required.issubset(pairs_df.columns):
            raise SystemExit(
                f"Файл {args.pairs} должен содержать колонки {required}. "
                f"Найдено: {list(pairs_df.columns)}"
            )
        for idx, row in pairs_df.iterrows():
            name = str(row.get('reaction', f'pair_{idx + 1}'))
            product = row.get('product')
            if pd.isna(product) or product == '':
                product = None
            rows.extend(analyze_reaction(name,
                                         str(row['reactant']),
                                         str(row['ts']),
                                         str(product) if product else None))

    # Режим 3: папка со всеми log-файлами
    elif args.dir:
        files = sorted(glob.glob(os.path.join(args.dir, '*.log')))
        if not files:
            raise SystemExit(f'В папке {args.dir} нет log-файлов.')
        for f in files:
            res = analyze_log(f)
            row = {'role': 'file', 'reaction': None, 'status_ts': None,
                   'Ea_kcal': None, 'dE_reaction_kcal': None}
            row.update({k: v for k, v in res.items() if k != 'path'})
            rows.append(row)

    # Режим 4: просто список файлов
    elif args.files:
        for f in args.files:
            res = analyze_log(f)
            row = {'role': 'file', 'reaction': None, 'status_ts': None,
                   'Ea_kcal': None, 'dE_reaction_kcal': None}
            row.update({k: v for k, v in res.items() if k != 'path'})
            rows.append(row)

    else:
        raise SystemExit('Укажите хотя бы один log-файл или один из режимов.')

    return rows


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='Анализ готовых log-файлов Gaussian для поиска TS '
                    '(лабораторная работа № 22, задание 7).'
    )
    parser.add_argument('files', nargs='*',
                        help='Один или несколько log-файлов')
    parser.add_argument('--dir',
                        help='Папка, в которой сканируются все .log-файлы')
    parser.add_argument('--reactant',
                        help='log-файл реагента (для расчёта Ea)')
    parser.add_argument('--ts',
                        help='log-файл переходного состояния')
    parser.add_argument('--product',
                        help='log-файл продукта (для расчёта dE реакции)')
    parser.add_argument('--name', default='reaction',
                        help='Имя реакции (для режима одной пары)')
    parser.add_argument('--pairs',
                        help='CSV-файл со столбцами '
                             'reaction,reactant,ts[,product]')
    parser.add_argument('--csv', default='ts_analysis.csv',
                        help='Имя выходного CSV-файла')
    args = parser.parse_args()

    rows = collect_rows(args)
    df = pd.DataFrame(rows)

    # Удобный порядок колонок
    preferred = ['role', 'reaction', 'file', 'normal_termination',
                 'E_Ha', 'n_atoms', 'n_freqs', 'n_imag',
                 'imag_freq_cm-1', 'status_ts',
                 'Ea_kcal', 'dE_reaction_kcal', 'error']
    df = df[[c for c in preferred if c in df.columns]]

    df.to_csv(args.csv, index=False)

    print(df.to_string(index=False))
    print(f'\nРезультаты сохранены в {args.csv}')

    # Краткая сводка по TS
    if 'status_ts' in df.columns:
        ts_rows = df[df['role'] == 'ts']
        if not ts_rows.empty:
            ok = (ts_rows['status_ts'] == 'ok_one_imaginary').sum()
            total = len(ts_rows)
            print(f'\nTS с ровно одной мнимой частотой: {ok} из {total}')
            if ok < total:
                print('Проверьте строки со status_ts != ok_one_imaginary: '
                      'возможно, нужна другая стартовая геометрия или '
                      'более широкий поиск (QST3).')


if __name__ == '__main__':
    main()