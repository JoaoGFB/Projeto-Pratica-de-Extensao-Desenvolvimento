# HidroCity — Site e API de Notícias

## Estrutura do repositório
- `projetohidrocity/` — frontend (site estático publicado no Netlify)
- `api/` — backend Python (Flask) que expõe `/news`
- `.gitignore` — evita venv e arquivos sensíveis

## Rodando localmente

### Backend
```bash
cd api
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
export NEWS_API_KEY="SUA_CHAVE"   # PowerShell: $env:NEWS_API_KEY="SUA_CHAVE"
python app.py
```
A API ficará disponível em http://localhost:5000/news.

### Frontend
```
cd projetohidrocity
python -m http.server 8000
````
# abra http://localhost:8000
