from API import API_KEY
import requests

URL = "https://newsapi.org/v2/everything"

def buscar_noticias(query="", title=None, page_size=5):
    params = {
        "q": query,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY
    }

    if title:  # se quiser filtrar pelo título
        params["qInTitle"] = title

    response = requests.get(URL, params=params)
    data = response.json()

    noticias_formatadas = []
    if data.get("articles"):
        for article in data["articles"]:
            noticias_formatadas.append({
                "titulo": article.get("title"),
                "fonte": article.get("source", {}).get("name"),
                "link": article.get("url"),
                "resumo": article.get("description") or "Sem resumo disponível",
                "publicado_em": article.get("publishedAt")
            })

    return noticias_formatadas