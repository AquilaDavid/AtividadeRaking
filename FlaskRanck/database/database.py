import sqlite3

DB_NAME = "instituicoesensino.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            co_entidade TEXT,
            no_entidade TEXT,
            no_uf TEXT,
            sg_uf TEXT,
            co_uf TEXT,
            no_municipio TEXT,
            co_municipio TEXT,
            no_mesorregiao TEXT,
            co_mesorregiao TEXT,
            no_microrregiao TEXT,
            co_microrregiao TEXT,
            nu_ano_censo INTEGER,
            no_regiao TEXT,
            co_regiao TEXT,
            qt_mat_bas INTEGER,
            qt_mat_prof INTEGER,
            qt_mat_eja INTEGER,
            qt_mat_esp INTEGER,
            qt_mat_fund INTEGER,
            qt_mat_inf INTEGER,
            qt_mat_med INTEGER,
            qt_mat_zr_na INTEGER,
            qt_mat_zr_rur INTEGER,
            qt_mat_zr_urb INTEGER,
            qt_mat_total INTEGER
        )
    """)
    conn.commit()
    conn.close()
