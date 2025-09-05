# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from news_api import buscar_noticias
import datetime
import os

app = Flask(__name__)
CORS(app)  # permite fetch do frontend hospedado em outro domínio

# cache simples em memória
cache = {
    "noticias": [],
    "ultima_atualizacao": None
}

CACHE_SEGUNDOS = int(os.getenv("CACHE_SECONDS", 86400))  # padrão 24h

@app.route("/news")
def news_endpoint():
    agora = datetime.datetime.utcnow()
    ultima = cache["ultima_atualizacao"]

    if (ultima is None) or ((agora - ultima).total_seconds() > CACHE_SEGUNDOS):
        cache["noticias"] = buscar_noticias(query="", title="água", page_size=6)
        cache["ultima_atualizacao"] = agora

    return jsonify(cache["noticias"])

if __name__ == "__main__":
    # Para teste local: python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
