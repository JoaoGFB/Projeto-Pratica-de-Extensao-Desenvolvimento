# news_api.py
import os
import requests

API_KEY = os.getenv("NEWS_API_KEY")  # defina no seu ambiente
URL = "https://newsapi.org/v2/everything"

def buscar_noticias(query="", title=None, page_size=5):
    params = {
        "q": query,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY
    }

    if title:
        params["qInTitle"] = title

    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Erro ao acessar NewsAPI:", e)
        return []

    noticias_formatadas = []
    for article in data.get("articles", []):
        noticias_formatadas.append({
            "titulo": article.get("title"),
            "fonte": article.get("source", {}).get("name"),
            "link": article.get("url"),
            "resumo": article.get("description") or "Sem resumo disponível",
            "publicado_em": article.get("publishedAt")
        })

    return noticias_formatadas
