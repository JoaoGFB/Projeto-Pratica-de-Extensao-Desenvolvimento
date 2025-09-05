# main.py
from news_api import buscar_noticias

if __name__ == "__main__":
    noticias = buscar_noticias(query="", title="água", page_size=5)
    if noticias:
        for n in noticias:
            print("Título:", n["titulo"])
            print("Fonte:", n["fonte"])
            print("Link:", n["link"])
            print("Resumo:", (n["resumo"] or "")[:150], "...")
            print("Publicado em:", n["publicado_em"])
            print("-" * 80)
    else:
        print("Nenhuma notícia encontrada.")
