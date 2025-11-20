from flask import Flask, jsonify, request
from models.censoescolar2024 import load_json_to_db
from database.database import get_db_connection

app = Flask(__name__)

load_json_to_db()

@app.route('/escolas', methods=['GET'])
def get_escolas():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    print(f"Requisição: listar escolas - página {page}, {per_page} por página")
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()
    escolas = cursor.execute(
        'SELECT * FROM censoescolar2024 LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    total = cursor.execute('SELECT COUNT(*) FROM censoescolar2024').fetchone()[0]
    conn.close()
    result = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': (total + per_page - 1) // per_page,
        'data': [dict(escola) for escola in escolas]
    }
    return jsonify(result)

@app.route('/escolas/<codigo>', methods=['GET'])
def get_escola(codigo):
    print(f"Requisição: buscar escola código {codigo}")
    conn = get_db_connection()
    escola = conn.execute('SELECT * FROM censoescolar2024 WHERE codigo = ?', (codigo,)).fetchone()
    conn.close()
    if escola:
        return jsonify(dict(escola))
    return jsonify({'error': 'Escola não encontrada'}), 404

if __name__ == '__main__':
    print("Iniciando API Flask...")
    app.run(debug=True)
