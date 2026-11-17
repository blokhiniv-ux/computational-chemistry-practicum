import database

DRUGS = [
    ("Парацетамол", "CC(=O)Nc1ccc(O)cc1"),
    ("Аспирин", "CC(=O)Oc1ccccc1C(=O)O"),
    ("Кофеин", "Cn1c(=O)c2c(ncn2C)n(C)c1=O"),
    ("Амоксициллин", "CC1(C)[C@@H]2SC([C@H](NC(=O)[C@@H](N)c3ccc(O)cc3)C(=O)O)N2C1=O"),
    ("Метформин", "CN(C)C(=N)NC(=N)N"),
    ("Аторвастатин", "CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccc(F)cc2)c(-c2ccccc2)n1CC[C@H](O)C[C@H](O)CC(=O)O"),
    ("Пенициллин G", "CC1(C)[C@@H]2SC([C@H](NC(=O)Cc3ccccc3)C(=O)O)N2C1=O"),
    ("Омепразол", "COc1ccc2[nH]c(nc2c1)S(=O)Cc1ncc(C)c(OC)c1C"),
    ("Диазепам", "CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21"),
    ("Варфарин", "CC(=O)CC(c1ccccc1)C1=C(O)c2ccccc2OC1=O"),
    ("Фуросемид", "NS(=O)(=O)c1cc(Cl)c(N)cc1Cc1occc1C(=O)O"),
    ("Пропранолол", "CC(C)NCC(O)COc1cccc2ccccc12"),
    ("Сальбутамол", "CC(C)(C)NCC(O)c1cc(CO)ccc1O"),
    ("Флуоксетин", "CNCCC(c1ccccc1)Oc1ccc(C(F)(F)F)cc1"),
    ("Сертралин", "CN[C@H]1CC[C@H](c2c1cccc2)c1ccc(c(c1)Cl)Cl"),
    ("Морфин", "CN1CC[C@]23c4c5ccc(O)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5"),
    ("Кодеин", "COc1ccc2c3c1O[C@H]1[C@@H](O)C=C[C@H]4[C@@H]1N(CC[C@]234)C"),
    ("Трамадол", "CN(C)CC1CCCCC1(c1cccc(OC)c1)O"),
    ("Лидокаин", "CCN(CC)CC(=O)Nc1c(C)cccc1C"),
    ("Прокаин", "CCN(CC)CCOC(=O)c1ccc(N)cc1"),
    ("Напроксен", "COc1ccc2ccccc2c1[C@@H](C)C(=O)O"),
    ("Диклофенак", "O=C(O)Cc1ccccc1Nc1c(Cl)cccc1Cl"),
    ("Целекоксиб", "Cc1ccc(-c2cc(C(F)(F)F)nn2-c2ccc(S(N)(=O)=O)cc2)cc1"),
    ("Преднизолон", "C[C@]12C[C@@H]([C@H]3[C@H]([C@@H]1CC[C@@]2(C(=O)CO)O)CCC4=CC(=O)C=C[C@]34C)O"),
    ("Дексаметазон", "C[C@@H]1C[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@@]4([C@]3([C@H](C[C@@]2([C@]1(C(=O)CO)O)C)O)F)C"),
    ("Амлодипин", "CCOC(=O)C1=C(CN)NC(C)=C(C(=O)OC)C1c1ccccc1Cl"),
    ("Нифедипин", "COC(=O)C1=C(C)NC(C)=C(C(=O)OC)C1c1ccccc1[N+](=O)[O-]"),
    ("Верапамил", "CC(C)C(CCCN(C)CCC1=CC(=C(C=C1)OC)OC)(C#N)C2=CC(=C(C=C2)OC)OC"),
    ("Дилтиазем", "CC(=O)O[C@@H]1[C@@H](SC2=CC=CC=C2N(C1=O)CCN(C)C)C3=CC=C(C=C3)OC"),
    ("Лозартан", "CCCCC1=NC(=C(Cl)N1Cc1ccc(-c2ccccc2-c2nnn[nH]2)cc1)CO"),
    ("Эналаприл", "CCOC(=O)[C@@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O"),
    ("Каптоприл", "C[C@H](CS)C(=O)N1CCC[C@H]1C(=O)O"),
    ("Симвастатин", "CCC(C)(C)C(=O)O[C@H]1C[C@H](C=C2[C@H]1[C@H]([C@H](C=C2)C)CC[C@@H]3C[C@H](CC(=O)O3)O)C"),
    ("Розувастатин", "CC(C)C1=NC(=NC(=C1/C=C/[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)N(C)S(=O)(=O)C"),
    ("Клопидогрел", "COC(=O)[C@H](N1CCc2sccc2C1)c1ccccc1Cl"),
    ("Метопролол", "CC(C)NCC(O)COc1ccc(CCOC)cc1"),
    ("Атенолол", "CC(C)NCC(O)COc1ccc(CC(=O)N)cc1"),
    ("Ранитидин", "CN/C(=C\\[N+](=O)[O-])/NCCSCc1ccc(CN(C)C)o1"),
    ("Циметидин", "CNC(=NC#N)NCCSCc1nc[nH]c1C"),
    ("Цетиризин", "O=C(O)COCCN1CCN(CC1)C(c1ccccc1)c1ccc(Cl)cc1"),
    ("Лоратадин", "CCOC(=O)N1CCC(=C2c3ccccc3CCc3ncccc32)CC1"),
    ("Дифенгидрамин", "CN(C)CCOC(c1ccccc1)c1ccccc1"),
    ("Левотироксин", "N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)cc1I)C(=O)O"),
    ("Метотрексат", "CN(Cc1cnc2c(N)nc(N)nc2n1)c1ccc(C(=O)N[C@@H](CCC(=O)O)C(=O)O)cc1"),
    ("Силденафил", "CCCC1=NN(C2=C1N=C(NC2=O)C3=C(C=CC(=C3)S(=O)(=O)N4CCN(CC4)C)OCC)C"),
    ("Тадалафил", "CN1CC(=O)N2[C@@H](C1=O)CC1=C([C@H]2c2ccc3OCOc3c2)Nc2ccccc21"),
    ("Фентанил", "CCC(=O)N(c1ccccc1)C1CCN(CCc2ccccc2)CC1"),
    ("Амфетамин", "CC(N)Cc1ccccc1"),
    ("Метронидазол", "Cc1ncc([N+](=O)[O-])n1CCO"),
]

def main():
    conn = database.create_database()
    added = 0
    skipped = []
    try:
        for name, smiles in DRUGS:
            try:
                database.add_compound(conn, name, smiles)
                added += 1
            except ValueError as exc:
                # Повторный запуск не должен аварийно завершать скрипт.
                skipped.append(f"{name}: {exc}")
        print(f"Добавлено новых соединений: {added}")
        if skipped:
            print("Пропущены записи:")
            for message in skipped:
                print(" -", message)
        print("База данных готова. Теперь запустите: python app.py")
    finally:
        conn.close()

if __name__ == "__main__":
    main()