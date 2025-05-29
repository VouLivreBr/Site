import os
import json
import flask
from flask import Flask, render_template, request, redirect, url_for

# Configuração do sistema de arquivos
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)

# Carregando as traduções
with open(os.path.join(app.static_folder, 'translations.json'), 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Idiomas suportados
SUPPORTED_LANGUAGES = ['pt', 'en', 'es']
DEFAULT_LANGUAGE = 'pt'

# Middleware para detectar o idioma
@app.before_request
def detect_language():
    # Verificar se já existe um idioma na URL
    path_parts = request.path.split('/')
    if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
        flask.g.lang = path_parts[1]
        return
    
    # Verificar se existe um idioma na sessão
    if 'lang' in flask.session:
        flask.g.lang = flask.session['lang']
        return
    
    # Detectar idioma do navegador
    browser_lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    if browser_lang:
        flask.g.lang = browser_lang
    else:
        flask.g.lang = DEFAULT_LANGUAGE
    
    # Salvar na sessão
    flask.session['lang'] = flask.g.lang

# Rota para redirecionamento da raiz para o idioma padrão
@app.route('/')
def index():
    return redirect(f'/{flask.g.lang}')

# Rota para a página inicial em cada idioma
@app.route('/<lang>/')
def home(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/')
    
    return render_template(
        'index.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de roteiros
@app.route('/<lang>/roteiros')
def itineraries(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/roteiros')
    
    return render_template(
        'roteiros.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de blog
@app.route('/<lang>/blog')
def blog(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/blog')
    
    return render_template(
        'blog.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de destinos
@app.route('/<lang>/destinos')
def destinations(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/destinos')
    
    return render_template(
        'destinos.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de comunidade
@app.route('/<lang>/comunidade')
def community(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/comunidade')
    
    return render_template(
        'comunidade.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de loja
@app.route('/<lang>/loja')
def shop(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/loja')
    
    return render_template(
        'loja.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de perfil
@app.route('/<lang>/perfil')
def profile(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/perfil')
    
    return render_template(
        'perfil.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para a página de detalhes do roteiro
@app.route('/<lang>/roteiros/<roteiro_id>')
def itinerary_detail(lang, roteiro_id):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/roteiros/{roteiro_id}')
    
    return render_template(
        'roteiro_detalhe.html',
        lang=lang,
        translations=translations,
        current_path=request.path,
        roteiro_id=roteiro_id
    )

# Rota para a página de planos premium
@app.route('/<lang>/planos')
def plans(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/planos')
    
    return render_template(
        'planos.html',
        lang=lang,
        translations=translations,
        current_path=request.path
    )

# Rota para alternar idioma
@app.route('/change-language/<lang>')
def change_language(lang):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    flask.session['lang'] = lang
    
    # Redirecionar para a mesma página no novo idioma
    referer = request.headers.get('Referer')
    if referer:
        # Extrair o caminho atual e substituir o idioma
        path_parts = request.path.split('/')
        if len(path_parts) > 2:
            new_path = '/' + lang + '/' + '/'.join(path_parts[2:])
            return redirect(new_path)
    
    return redirect(f'/{lang}/')

# Configuração da sessão
app.secret_key = 'vou_livre_secret_key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
