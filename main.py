import os
import json
import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuração do sistema de arquivos
# Certifique-se de que esta linha está correta para seu projeto
# Ela adiciona o diretório pai ao PATH, útil se 'src' ou 'venv' estiverem em outro nível
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


app = Flask(__name__)

# --- Configurações do Flask e Banco de Dados ---
# Chave Secreta para segurança de sessões. Use uma variável de ambiente em produção!
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SUA_CHAVE_SECRETA_PADRAO_MUITO_FORTE_AQUI_123'

# Configuração da URI do Banco de Dados
# Em produção no Render, ele usará a DATABASE_URL. Localmente, usará sqlite:///site.db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa avisos de rastreamento de modificações, economiza memória

# Inicialização do SQLAlchemy e Flask-Migrate (APENAS UMA VEZ)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- MODELOS DE BANCO DE DADOS ---
# Definição do modelo para as configurações gerais do site
class ConfiguracaoSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Caminho da imagem da logo (será salvo no sistema de arquivos e o caminho aqui)
    logo_url = db.Column(db.String(255), nullable=True, default='/static/images/default_logo.png')

    # Cores principais do site (ex: cor_primaria, cor_secundaria)
    cor_primaria = db.Column(db.String(7), default='#1a73e8') # Exemplo de cor azul
    cor_secundaria = db.Column(db.String(7), default='#ffffff') # Exemplo de cor branca

    # Texto principal da pagina inicial
    titulo_pagina_inicial = db.Column(db.String(255), default='Bem-vindo ao Vou Livre BR!')
    subtitulo_pagina_inicial = db.Column(db.String(255), default='Sua Aventura Começa Aqui!')

    # Você pode adicionar outros campos aqui conforme as necessidades globais do seu site
    # Por exemplo: link_instagram, link_facebook, etc.

    def __repr__(self):
        return f'<ConfiguracaoSite {self.id}>'

# --- Carregando as traduções (pode permanecer aqui ou ser dinâmico no futuro) ---
with open(os.path.join(app.static_folder, 'translations.json'), 'r', encoding='utf-8') as f:
    translations = json.load(f)

# --- Idiomas suportados ---
SUPPORTED_LANGUAGES = ['pt', 'en', 'es']
DEFAULT_LANGUAGE = 'pt'

# --- Middleware para detectar o idioma ---
@app.before_request
def detect_language():
    # A session precisa ser definida no app.config['SECRET_KEY'] para funcionar
    # Verificar se já existe um idioma na URL
    path_parts = request.path.split('/')
    if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
        flask.g.lang = path_parts[1]
        return
    
    # Verificar se existe um idioma na sessão
    if 'lang' in session: # Use 'session' do flask import
        flask.g.lang = session['lang']
        return
    
    # Detectar idioma do navegador
    browser_lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    if browser_lang:
        flask.g.lang = browser_lang
    else:
        flask.g.lang = DEFAULT_LANGUAGE
    
    # Salvar na sessão
    session['lang'] = flask.g.lang # Use 'session' do flask import


# --- Rotas da Aplicação ---

# Rota para redirecionamento da raiz para o idioma padrão
@app.route('/')
def index():
    return redirect(f'/{flask.g.lang}')

# Rota para a página inicial em cada idioma
@app.route('/<lang>/')
def home(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/')
    
    # Exemplo de como carregar as configurações do site
    # Lembre-se que isso vai buscar do banco de dados agora
    site_config = ConfiguracaoSite.query.first()
    if site_config is None:
        # Cria uma configuração padrão se ainda não existir no banco
        site_config = ConfiguracaoSite()
        db.session.add(site_config)
        db.session.commit()

    return render_template(
        'index.html',
        lang=lang,
        translations=translations,
        current_path=request.path,
        site_config=site_config # Passando as configurações para o template
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
    if lang not in SUPPORTED_LANGES:
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
    
    session['lang'] = lang # Use 'session' do flask import
    
    # Redirecionar para a mesma página no novo idioma
    referer = request.headers.get('Referer')
    if referer:
        # Extrair o caminho atual e substituir o idioma
        path_parts = request.path.split('/')
        if len(path_parts) > 2:
            new_path = '/' + lang + '/' + '/'.join(path_parts[2:])
            return redirect(new_path)
    
    return redirect(f'/{lang}/')


# --- Execução da Aplicação ---
# Apenas um bloco if __name__ == '__main__': para toda a execução
if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas do banco de dados se não existirem
        # IMPORTANTE: Em produção, use 'flask db upgrade' no Render, não db.create_all()
        db.create_all() 
        
        # Garante que sempre haja uma entrada de Configuração do Site
        if ConfiguracaoSite.query.first() is None:
            default_config = ConfiguracaoSite()
            db.session.add(default_config)
            db.session.commit()
            print("Configuração padrão do site criada no banco de dados.")

    # Inicia o servidor de desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)