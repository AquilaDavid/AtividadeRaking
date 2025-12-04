from flask import Blueprint, jsonify
from database.database import get_db_connection

bp = Blueprint("instituicoes", __name__)

@bp.get("/instituicoesensino/ranking/<int:ano>")
def ranking(ano):
    if ano not in [2022, 2023, 2024]:
        return jsonify({"erro": "Ano inválido"}), 400

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT *
        FROM instituicoes
        WHERE nu_ano_censo = ?
        ORDER BY qt_mat_total DESC
        LIMIT 10
    """, (ano,)).fetchall()
    conn.close()

    resultado = []
    ranking = 1

    for row in rows:
        item = dict(row)
        item["nu_ranking"] = ranking
        resultado.append(item)
        ranking += 1

    return jsonify(resultado)
