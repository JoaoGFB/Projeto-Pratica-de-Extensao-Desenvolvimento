from flask import Flask, render_template
from news_api import buscar_noticias
import datetime

app = Flask(__name__)

# Cache em memória
cache = {
    "noticias": [],
    "ultima_atualizacao": None
}

@app.route("/")
def home():
    agora = datetime.datetime.now()
    
    # Atualiza se nunca buscou ou se já passaram 24h (86400 segundos)
    if (cache["ultima_atualizacao"] is None or
        (agora - cache["ultima_atualizacao"]).total_seconds() > 86400):
        
        cache["noticias"] = buscar_noticias(query="", title="água")
        cache["ultima_atualizacao"] = agora

    return render_template("index.html", noticias=cache["noticias"])

if __name__ == "__main__":
    app.run(debug=True)