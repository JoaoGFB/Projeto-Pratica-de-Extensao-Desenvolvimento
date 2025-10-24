from news_api import buscar_noticias
from datetime import datetime

def atualizar_cache_noticias():
    consultas = {
        "mundo": ["Mundo", "água", "saneamento"],
        "Brasil": ["Brasil", "água", "saneamento"],
        "Paraná": ["Paraná", "água", "saneamento"],
        "Londrina": ["Londrina", "água", "saneamento"]
    }

    noticias_por_categoria = {}
    for chave, termos in consultas.items():
        if len(termos) > 1:
            # A partir do primeiro elemento ele faz uma query com OR, com o elemento 0 ele faz um AND obrigátorio para procurar
            #precisa fazer esse f"" para substituir pelos valores.
            query = f"({' OR '.join(termos[1:])}) AND {termos[0]}"
        else:
            query = termos[0]

        # O primeiro termo continua sendo usado como título
        title = termos[0]
        noticias_por_categoria[chave] = buscar_noticias(query=query, title=title, page_size=6)

    return noticias_por_categoria
if __name__ == "__main__":
    print("Buscando notícias...")
    agora = datetime.utcnow()
    noticias = atualizar_cache_noticias()

    for categoria, lista in noticias.items():
        print(f"\n{'='*80}")
        print(f" {categoria.upper()} — {len(lista)} notícias encontradas")
        print(f"{'='*80}")
        for n in lista:
            print(f"• {n['titulo']} ({n['fonte']})")
        print("-" * 80)

    print(f"\n Finalizado às {agora.isoformat()} UTC")