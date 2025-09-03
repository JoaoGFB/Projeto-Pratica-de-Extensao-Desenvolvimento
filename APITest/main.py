from news_api import buscar_noticias

noticias = buscar_noticias(query="", title="água")

if noticias:
    for n in noticias:
        print("Título:", n["titulo"])
        print("Fonte:", n["fonte"])
        print("Link:", n["link"])
        print("Resumo:", n["resumo"][:150], "...")
        print("Publicado em:", n["publicado_em"])
        print("-" * 80)
else:
    print("Nenhuma notícia encontrada.")