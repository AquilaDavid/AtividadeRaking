import pandas as pd
import sqlite3
import os

DB_NAME = "instituicoesensino.db"

def carregar_csv(caminho, ano):
    df = pd.read_csv(caminho, sep=";", dtype=str, encoding="latin1")
    df.columns = [c.lower().strip() for c in df.columns]

    campos = [
        "co_entidade", "no_entidade", "no_uf", "sg_uf", "co_uf",
        "no_municipio", "co_municipio", "no_mesorregiao", "co_mesorregiao",
        "no_microrregiao", "co_microrregiao", "no_regiao", "co_regiao",
        "qt_mat_bas", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp",
        "qt_mat_fund", "qt_mat_inf", "qt_mat_med",
        "qt_mat_zr_na", "qt_mat_zr_rur", "qt_mat_zr_urb"
    ]

    for col in campos:
        if col not in df:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["qt_mat_total"] = (
        df["qt_mat_bas"] + df["qt_mat_prof"] + df["qt_mat_eja"] + df["qt_mat_esp"] +
        df["qt_mat_fund"] + df["qt_mat_inf"] + df["qt_mat_med"] +
        df["qt_mat_zr_na"] + df["qt_mat_zr_rur"] + df["qt_mat_zr_urb"]
    )

    df["nu_ano_censo"] = int(ano)

    df = df[[
        "co_entidade", "no_entidade", "no_uf", "sg_uf", "co_uf", "no_municipio",
        "co_municipio", "no_mesorregiao", "co_mesorregiao", "no_microrregiao",
        "co_microrregiao", "nu_ano_censo", "no_regiao", "co_regiao",
        "qt_mat_bas", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp", "qt_mat_fund",
        "qt_mat_inf", "qt_mat_med", "qt_mat_zr_na", "qt_mat_zr_rur",
        "qt_mat_zr_urb", "qt_mat_total"
    ]]

    conn = sqlite3.connect(DB_NAME)
    df.to_sql("instituicoes", conn, if_exists="append", index=False)
    conn.close()


def load_all_csvs():
    anos = {
        "microdados_ed_basica_2022.csv": 2022,
        "microdados_ed_basica_2023.csv": 2023,
        "microdados_ed_basica_2024.csv": 2024
    }

    base = os.path.dirname(os.path.dirname(__file__))

    for nome, ano in anos.items():
        caminho = os.path.join(base, nome)
        if os.path.exists(caminho):
            carregar_csv(caminho, ano)
