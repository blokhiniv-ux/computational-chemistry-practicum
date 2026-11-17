"""
Извлечение экспериментальных данных IC50 из ChEMBL
для мишени CHEMBL243 (HIV-1 protease).

Результат: raw_data.csv — исходные записи
без удаления повторных измерений.

Установка зависимостей:
    pip install requests pandas

Скрипт обращается к REST API ChEMBL напрямую
и не использует chembl_webresource_client.
"""

import sys
import time

import pandas as pd
import requests

BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"
TARGET_ID = "CHEMBL243"
OUTPUT_FILE = "raw_data.csv"
PAGE_SIZE = 1000
REQUEST_PAUSE = 0.25

OUTPUT_COLUMNS = [
    "activity_id",
    "molecule_chembl_id",
    "canonical_smiles",
    "standard_type",
    "standard_relation",
    "standard_value",
    "standard_units",
    "standard_flag",
    "assay_chembl_id",
    "assay_type",
    "assay_description",
    "bao_label",
    "document_chembl_id",
    "pchembl_value",
]


def check_target():
    """Проверяет, что мишень существует, и выводит её название."""
    print("Проверка выбранной мишени...")

    url = f"{BASE_URL}/target/{TARGET_ID}.json"

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Ошибка при обращении к ChEMBL:", e)
        sys.exit(1)

    target_info = response.json()

    if target_info.get("target_chembl_id") != TARGET_ID:
        print(f"Мишень {TARGET_ID} не найдена.")
        sys.exit(1)

    print("Мишень:", target_info.get("pref_name"))
    print("Идентификатор:", TARGET_ID)


def download_activities():
    """Загружает все страницы данных IC50 (пагинация)."""
    print("\nЗагрузка данных активности IC50...")

    url = f"{BASE_URL}/activity.json"
    records = []
    offset = 0
    total_count = None

    while True:
        params = {
            "target_chembl_id": TARGET_ID,
            "standard_type": "IC50",
            "standard_value__isnull": "false",
            "limit": PAGE_SIZE,
            "offset": offset,
        }

        try:
            response = requests.get(url, params=params, timeout=90)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Ошибка сети при обращении к ChEMBL:", e)
            sys.exit(1)

        data = response.json()
        page = data.get("activities", [])

        if total_count is None:
            page_meta = data.get("page_meta") or {}
            total_count = page_meta.get("total_count")

        if not page:
            break

        records.extend(page)
        offset += len(page)

        if total_count is not None:
            print(f"Получено записей: {len(records)} из {total_count}")
        else:
            print(f"Получено записей: {len(records)}")

        if total_count is not None and len(records) >= total_count:
            break
        if len(page) < PAGE_SIZE:
            break

        time.sleep(REQUEST_PAUSE)

    return records


def save_raw_data(records):
    """Сохраняет исходные записи в CSV без удаления повторов."""
    if not records:
        print("\nЗаписи об активности не найдены.")
        return

    df = pd.DataFrame(records)

    # Гарантируем наличие всех нужных столбцов
    for column in OUTPUT_COLUMNS:
        if column not in df.columns:
            df[column] = None

    # Сохраняем фиксированный набор и порядок столбцов
    df = df[OUTPUT_COLUMNS]

    # Дубликаты намеренно не удаляем:
    # строки могут относиться к разным экспериментам.
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\nЗагрузка завершена.")
    print("Количество исходных записей:", len(df))

    print("\nТипы активности:")
    print(df["standard_type"].value_counts(dropna=False))

    print("\nЕдиницы измерения:")
    print(df["standard_units"].value_counts(dropna=False))

    print("\nТипы отношений:")
    print(df["standard_relation"].value_counts(dropna=False))

    print("\nФайл сохранён:", OUTPUT_FILE)


def main():
    check_target()
    records = download_activities()
    save_raw_data(records)


if __name__ == "__main__":
    main()