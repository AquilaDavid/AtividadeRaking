from flask import Flask
from database.database import init_db
from models.censoescolar_loader import load_all_csvs
from routes.instituicoes import bp
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Logging
handler = RotatingFileHandler("app.log", maxBytes=5000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Inicializa DB
init_db()

# Carrega CSVs
load_all_csvs()

# Rotas
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
