from database.database import get_db_connection
import json

def create_table_censoescolar2024():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS censoescolar2024 (
            codigo TEXT PRIMARY KEY,
            nome TEXT,
            uf TEXT,
            municipio TEXT,
            qt_mat_bas INTEGER,
            qt_mat_inf INTEGER,
            qt_mat_fund INTEGER,
            qt_mat_med INTEGER,
            qt_mat_prof INTEGER,
            qt_mat_esp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_many_censoescolar2024(escolas):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = [
        (
            e.get('codigo'),
            e.get('nome'),
            e.get('uf'),
            e.get('municipio'),
            e.get('qt_mat_bas', 0),
            e.get('qt_mat_inf', 0),
            e.get('qt_mat_fund', 0),
            e.get('qt_mat_med', 0),
            e.get('qt_mat_prof', 0),
            e.get('qt_mat_esp', 0)
        ) for e in escolas
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO censoescolar2024
        (codigo, nome, uf, municipio, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_esp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)
    conn.commit()
    conn.close()
    print(f"{len(escolas)} escolas inseridas de uma vez com sucesso!")

def load_json_to_db(json_path='data/censoJson.json', batch_size=5000):
    create_table_censoescolar2024()
    with open(json_path, encoding='utf-8') as f:
        escolas = json.load(f)
        total = len(escolas)
        print(f"Carregando {total} escolas no banco em lotes de {batch_size}...")
        for i in range(0, total, batch_size):
            batch = escolas[i:i+batch_size]
            insert_many_censoescolar2024(batch)
            print(f"  {min(i+batch_size, total)}/{total} escolas carregadas")
    print("Todos os dados foram carregados com sucesso!")
