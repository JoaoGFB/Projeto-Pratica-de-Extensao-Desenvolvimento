# app.py
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from news_api import buscar_noticias
import datetime
import os
from google.genai import Client
import time
import threading


client = Client()
GEMINI_MODEL = 'gemini-2.5-flash'
DELAY_DE_CHAMADA = 6.2#Tem um limite para a camada gratis e é bom um delay a cada chamada


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app = Flask(
    __name__,
    root_path=project_root, # Define a PASTA MÃE como raiz
    # Caminhos de templeste e arquivos estáticos:
    template_folder='projetohidrocity/templates',
    static_folder='projetohidrocity/static'
)
CORS(app)  # permite fetch do frontend hospedado em outro domínio



# cache simples em memória
cache = {
    "noticias": [],
    "ultima_atualizacao": None
}

atualizando_noticias = False
CACHE_SEGUNDOS = int(os.getenv("CACHE_SECONDS", 86400))  # padrão 24h

#COM API DO GEMINI
def noticia_relevante(titulo, sumario):
    #Uso da API do Gemini para classificação se a notícia compensa.
    #Prompt para a API
   prompt = (
    "Classifique a seguinte notícia. A notícia deve ser sobre 'água', 'saneamento', 'recursos hídricos', "
    "meio ambiente hídrico ou problemas de saúde pública relacionados à água. "
    # MUDANÇA AQUI: Simplificando a regra de exclusão
    "EXCLUA notícias se o TEMA PRINCIPAL for esportes aquáticos, previsão do tempo/chuva sem contexto de crise, ou fofoca de celebridades. "
    f"Título: {titulo}. Resumo: {sumario}. "
    f"Responda APENAS com a palavra 'SIM' se for relevante, ou 'NÃO' se for irrelevante."
)
   for tentativa in range(2):
    try:
        #Tempo para erros
        time.sleep(DELAY_DE_CHAMADA)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            #Config de criatividade
            config={"temperature":0.0}
            )
        return "SIM" in response.text.upper()
    except Exception as e:
        #Se erro
        if tentativa == 0 and "503" in str(e):
            print(f"ERRO 503 DETECTADO. Tentando novamente em 5 segundos.")
            time.sleep(5)
            continue
        print(f"Erro fatal na API Gemini ({GEMINI_MODEL}): {e}. Mantendo notícia por segurança.")
        return True # Mantém a notícia para evitar que o cache fique vazio
    return True

def processar_cache_noticias_com_ai():
    #start_time = time.time()
    global cache
    global atualizando_noticias
    consultas = {
        "mundo": ["Mundo", "água", "saneamento"],
        "Brasil": ["Brasil", "água", "saneamento"],
        "Paraná": ["Paraná", "água", "saneamento"],
        "Londrina": ["Londrina", "água", "saneamento"]
    }

    noticias_filtradas_por_categoria = {}
    for chave, termos in consultas.items():
        if len(termos) > 1:
            # A partir do primeiro elemento ele faz uma query com OR, com o elemento 0 ele faz um AND obrigátorio para procurar
            #precisa fazer esse f"" para substituir pelos valores.
            query = f"({' OR '.join(termos[1:])}) AND {termos[0]}"
        else:
            query = termos[0]

        # O primeiro termo continua sendo usado como título
        title = termos[0]
        noticias_brutas = buscar_noticias(query=query, title=title, page_size=6)
        noticias_final =[]

        for noticia in noticias_brutas:
            if noticia_relevante(noticia.get('titulo',''), noticia.get('resumo','')):
                noticias_final.append(noticia)

        noticias_filtradas_por_categoria[chave] = noticias_final
        cache["noticias"] = noticias_filtradas_por_categoria
        cache["ultima_atualizacao"] = datetime.datetime.utcnow()
        atualizando_noticias = False
    #end_time = time.time()
    #duration = end_time - start_time
    #print(f"TEMPO TOTAL DE ATUALIZAÇÃO DO CACHE: {duration:.2f} segundos")

    return noticias_filtradas_por_categoria


def inicializacao_cache_doDia():
    """Roda sem a API do Gemini"""
    consultas = {
        "mundo": ["Mundo", "água", "saneamento"],
        "Brasil": ["Brasil", "água", "saneamento"],
        "Paraná": ["Paraná", "água", "saneamento"],
        "Londrina": ["Londrina", "água", "saneamento"]
    }
    noticias_filtradas_por_categoria = {}
    for chave, termos in consultas.items():
        query = f"({' OR '.join(termos[1:])}) AND {termos[0]}" if len(termos) > 1 else termos[0]
        # Usamos page_size=6 aqui também para consistência na busca
        noticias_filtradas_por_categoria[chave] = buscar_noticias(query=query, title=termos[0], page_size=6)
   
    return noticias_filtradas_por_categoria

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/news")
def news_endpoint():
    global cache
    global atualizando_noticias
    agora = datetime.datetime.utcnow()
    ultima = cache["ultima_atualizacao"]
    cache_vazio = not cache["noticias"]
    cache_expirou = (ultima is None) or ((agora - ultima).total_seconds() > CACHE_SEGUNDOS)
    if cache_vazio:
        cache["noticias"] = inicializacao_cache_doDia()
        # Não seta ultima_atualizacao para forçar a thread a rodar logo em seguida.

    # 2. Se o cache expirou e NENHUMA thread está rodando, INICIA a thread lenta.
    if cache_expirou and not atualizando_noticias:
        atualizando_noticias = True
        thread = threading.Thread(target=processar_cache_noticias_com_ai)
        thread.start()
    return jsonify(cache["noticias"])

if __name__ == "__main__":
    # Para teste local: python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), threaded=True)

#SEM API DO GEMINI
def atualizar_cache_noticias():
    consultas = {
        "mundo": ["Mundo", "água", "saneamento"],
        "Brasil": ["Brasil", "água", "saneamento"],
        "Paraná": ["Paraná", "água", "saneamento"],
        "Londrina": ["Londrina", "água", "saneamento"]
    }
    noticias_filtradas_por_categoria = {}
    for chave, termos in consultas.items():
        if len(termos) > 1:
            # Constrói a query com AND e OR
            query = f"({' OR '.join(termos[1:])}) AND {termos[0]}"
        else:
            query = termos[0]
        # O primeiro termo continua sendo usado como título
        title = termos[0]
        noticias_brutas = buscar_noticias(query=query, title=title, page_size=7)
        noticias_filtradas_por_categoria[chave] = noticias_brutas
    return noticias_filtradas_por_categoria
