import os
import json # Pode remover se i18n_config.py lidar com a carga do JSON
import flask
from flask import Flask, render_template, request, redirect, url_for, session, g # Adicionado 'g'
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# --- Importar a configuração da biblioteca i18n ---
# Certifique-se de que i18n_config.py esteja na mesma pasta ou no seu PYTHONPATH
import i18n # Importa a biblioteca i18n, que já estará configurada por i18n_config.py
from i18n_config import configure_i18n_lib # Importa e chama a função de configuração

# Configuração do sistema de arquivos
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


app = Flask(__name__)

# --- Configurações do Flask e Banco de Dados ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SUA_CHAVE_SECRETA_PADRAO_MUITO_FORTE_AQUI_123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- MODELOS DE BANCO DE DADOS ---
class ConfiguracaoSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo_url = db.Column(db.String(255), nullable=True, default='/static/images/default_logo.png')
    cor_primaria = db.Column(db.String(7), default='#1a73e8')
    cor_secundaria = db.Column(db.String(7), default='#ffffff')
    titulo_pagina_inicial = db.Column(db.String(255), default='Bem-vindo ao Vou Livre BR!')
    subtitulo_pagina_inicial = db.Column(db.String(255), default='Sua Aventura Começa Aqui!')

    def __repr__(self):
        return f'<ConfiguracaoSite {self.id}>'

# --- Idiomas suportados ---
SUPPORTED_LANGUAGES = ['pt', 'en', 'es']
DEFAULT_LANGUAGE = 'pt'

# --- Middleware para detectar o idioma ---
@app.before_request
def detect_language():
    lang_code = DEFAULT_LANGUAGE # Define um padrão inicial

    # 1. Tenta pegar o idioma da URL (ex: /en/home)
    path_parts = request.path.split('/')
    if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
        lang_code = path_parts[1]
    
    # 2. Se não estiver na URL, tenta pegar da sessão
    elif 'lang' in session and session['lang'] in SUPPORTED_LANGUAGES:
        lang_code = session['lang']
    
    # 3. Se não estiver na sessão, tenta detectar do navegador
    else:
        browser_lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
        if browser_lang:
            lang_code = browser_lang
    
    # Define o idioma para a biblioteca i18n
    i18n.set('locale', lang_code)
    # Armazena o idioma na variável global `g` do Flask para acesso fácil nas templates e rotas
    g.lang = lang_code
    
    # Opcional: Garante que o idioma detectado ou da URL seja salvo na sessão para persistência
    if 'lang' not in session or session['lang'] != lang_code:
        session['lang'] = lang_code


# --- Rotas da Aplicação ---

# Rota para redirecionamento da raiz para o idioma padrão
@app.route('/')
def index():
    # Usa g.lang que foi definido no before_request
    return redirect(f'/{g.lang}/')

# Função auxiliar para passar parâmetros comuns para render_template
def render_translated_template(template_name, lang, **kwargs):
    return render_template(
        template_name,
        lang=lang,
        t=i18n.t, # Passa a função de tradução
        current_path=request.path,
        **kwargs
    )

# Rota para a página inicial em cada idioma
@app.route('/<lang>/')
@app.route('/<lang>/home')
def home(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/')
    
    # Garante que g.lang e o locale do i18n estão corretos para esta rota específica
    # (importante se a rota for acessada diretamente com um idioma específico na URL)
    i18n.set('locale', lang)
    g.lang = lang

    site_config = ConfiguracaoSite.query.first()
    if site_config is None:
        site_config = ConfiguracaoSite()
        db.session.add(site_config)
        db.session.commit()

    return render_translated_template(
        'index.html',
        lang=lang,
        site_config=site_config
    )

# Rotas de páginas estáticas e outras
@app.route('/<lang>/roteiros')
def itineraries(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/roteiros')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('roteiros.html', lang=lang)

@app.route('/<lang>/blog')
def blog(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/blog')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('blog.html', lang=lang)

@app.route('/<lang>/destinos')
def destinations(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/destinos')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('destinos.html', lang=lang)

@app.route('/<lang>/comunidade')
def community(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/comunidade')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('comunidade.html', lang=lang)

@app.route('/<lang>/loja')
def shop(lang):
    # Correção: 'SUPPORTED_LANGUAGES' ao invés de 'SUPPORTED_LANGES'
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/loja')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('loja.html', lang=lang)

@app.route('/<lang>/perfil')
def profile(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/perfil')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('perfil.html', lang=lang)

@app.route('/<lang>/roteiros/<roteiro_id>')
def itinerary_detail(lang, roteiro_id):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/roteiros/{roteiro_id}')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('roteiro_detalhe.html', lang=lang, roteiro_id=roteiro_id)

@app.route('/<lang>/planos')
def plans(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/planos')
    i18n.set('locale', lang)
    g.lang = lang
    return render_translated_template('planos.html', lang=lang)

# Rota para alternar idioma
@app.route('/change-language/<lang_code>') # Renomeado para evitar conflito com 'lang' de outras rotas
def change_language(lang_code):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    
    session['lang'] = lang_code # Salva o idioma na sessão
    
    # Tenta redirecionar para a mesma página no novo idioma
    referer = request.headers.get('Referer')
    if referer:
        # Analisa a URL de referência
        from urllib.parse import urlparse
        parsed_referer = urlparse(referer)
        
        # O caminho do referer é /<idioma>/caminho/restante
        path_parts = parsed_referer.path.split('/')
        
        # Verifica se o segundo elemento é um idioma suportado
        if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
            # Constrói o novo caminho com o novo idioma
            new_path_segments = [lang_code] + path_parts[2:]
            new_path = '/' + '/'.join(new_path_segments)
            return redirect(new_path)
    
    # Se não houver referer ou o parse falhar, redireciona para a home no novo idioma
    return redirect(f'/{lang_code}/')


# --- Execução da Aplicação ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        
        if ConfiguracaoSite.query.first() is None:
            default_config = ConfiguracaoSite()
            db.session.add(default_config)
            db.session.commit()
            print("Configuração padrão do site criada no banco de dados.")

    app.run(host='0.0.0.0', port=5000, debug=True)
