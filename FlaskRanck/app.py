from flask import Flask
from database.database import init_db
from models.censoescolar_loader import load_all_csvs
from routes.instituicoes import bp

app = Flask(__name__)

init_db()
load_all_csvs()

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
