from flask import Flask, jsonify
import pandas as pd
import json
import os
import unicodedata

app = Flask(__name__)

NE_NOMES = {
    "ALAGOAS",
    "BAHIA",
    "CEARA",
    "MARANHAO",
    "PARAIBA",
    "PERNAMBUCO",
    "PIAUI",
    "RIO GRANDE DO NORTE",
    "SERGIPE"
}

def remover_acentos(texto):
    if not isinstance(texto, str):
        return texto
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")


@app.route("/processar")
def processar_csv():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "data", "microdados_ed_basica_2024.csv")
    output_file = os.path.join(BASE_DIR, "censoJson.json")

    if not os.path.exists(csv_path):
        return jsonify({"erro": f"Arquivo NÃO encontrado: {csv_path}"}), 400

    resultados = []

    for chunk in pd.read_csv(csv_path, sep=";", dtype=str, chunksize=50000, encoding="latin1"):
        chunk["NO_UF"] = chunk["NO_UF"].astype(str).str.upper().apply(remover_acentos)
        chunk = chunk[chunk["NO_UF"].isin(NE_NOMES)]

        if chunk.empty:
            continue

        campos_mat = ["QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND",
                      "QT_MAT_MED", "QT_MAT_PROF", "QT_MAT_ESP"]

        for campo in campos_mat:
            chunk[campo] = pd.to_numeric(chunk[campo], errors="coerce").fillna(0).astype(int)

        for _, row in chunk.iterrows():
            resultados.append({
                "codigo": row["CO_ENTIDADE"],
                "nome": row["NO_ENTIDADE"],
                "uf": row["NO_UF"],
                "municipio": row["NO_MUNICIPIO"],
                "qt_mat_bas": row["QT_MAT_BAS"],
                "qt_mat_inf": row["QT_MAT_INF"],
                "qt_mat_fund": row["QT_MAT_FUND"],
                "qt_mat_med": row["QT_MAT_MED"],
                "qt_mat_prof": row["QT_MAT_PROF"],
                "qt_mat_esp": row["QT_MAT_ESP"]
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    return jsonify({
        "mensagem": "Processamento concluído!",
        "json_salvo_em": output_file,
        "registros": len(resultados)
    })


@app.route("/")
def home():
    return jsonify({"status": "API funcionando"})


if __name__ == "__main__":
    app.run(debug=True)
