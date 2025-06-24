import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

# --- DADOS TEMPORÁRIOS PARA OS ROTEIROS ---
# No futuro, isso virá de uma tabela do banco de dados.
DADOS_ROTEIROS = {
    "rio-classico": {
        "titulo_chave": "classic_rio_title",
        "titulo_padrao": "Rio Clássico - 3 dias",
        "descricao_chave": "classic_rio_description",
        "descricao_padrao": "Conheça os principais pontos turísticos do Rio de Janeiro em um roteiro completo de 3 dias.",
        "imagem_url": "/static/images/arpoador.jpg",
        "preco": "129,90",
        "rating": 4.5,
        "detalhes_longos": "Este roteiro de 3 dias é perfeito para quem visita o Rio pela primeira vez. No primeiro dia, exploramos o Cristo Redentor e o Pão de Açúcar. O segundo dia é dedicado às praias de Copacabana e Ipanema, com um pôr do sol inesquecível no Arpoador. O terceiro dia cobre o centro histórico, a Escadaria Selarón e os Arcos da Lapa."
    },
    "praias-rio": {
        "titulo_chave": "rio_beaches_title",
        "titulo_padrao": "Praias do Rio - 2 dias",
        "descricao_chave": "rio_beaches_description",
        "descricao_padrao": "Um fim de semana relaxante conhecendo as melhores praias da cidade maravilhosa.",
        "imagem_url": "/static/images/bondinho.jpg",
        "preco": "89,90",
        "rating": 4.0,
        "detalhes_longos": "Relaxe e aproveite o sol nas famosas praias do Rio. Este roteiro inclui um dia em Copacabana e Leme, e outro dia explorando as belezas de Ipanema e Leblon. Inclui dicas dos melhores quiosques e atividades na areia."
    },
    "rio-gastronomico": {
        "titulo_chave": "rio_gastronomy_title",
        "titulo_padrao": "Rio Gastronômico - 4 dias",
        "descricao_chave": "rio_gastronomy_description",
        "descricao_padrao": "Experimente o melhor da gastronomia carioca neste roteiro para verdadeiros amantes da boa comida.",
        "imagem_url": "/static/images/gastronomia-rj.jpg",
        "preco": "159,90",
        "rating": 4.8,
        "detalhes_longos": "Uma imersão nos sabores do Rio. Este roteiro te leva a restaurantes renomados, bares tradicionais da Lapa, feiras de rua e aulas de culinária para você aprender a fazer a sua própria feijoada e caipirinha."
    }
}

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

# --- INTERNACIONALIZAÇÃO (i18n) ---
# Carrega o arquivo de traduções
with open(os.path.join(app.static_folder, 'translations.json'), 'r', encoding='utf-8') as f:
    translations = json.load(f)

SUPPORTED_LANGUAGES = ['pt', 'en', 'es']
DEFAULT_LANGUAGE = 'pt'

@app.before_request
def detect_language():
    """Detecta o idioma e o armazena em `g.lang` para uso na requisição."""
    path_parts = request.path.split('/')
    lang_code = DEFAULT_LANGUAGE

    if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
        lang_code = path_parts[1]
    elif 'lang' in session:
        lang_code = session['lang']
    else:
        browser_lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
        if browser_lang:
            lang_code = browser_lang

    g.lang = lang_code
    session['lang'] = lang_code

def render_with_lang(template_name, **kwargs):
    """Função auxiliar para sempre passar variáveis comuns para os templates."""
    return render_template(
        template_name,
        lang=g.lang,
        translations=translations,
        current_path=request.path,
        **kwargs
    )


# --- ROTAS PRINCIPAIS ---

@app.route('/')
def index():
    """Redireciona a rota raiz (/) para a home com o idioma detectado."""
    return redirect(url_for('home', lang=g.lang))

@app.route('/<string:lang>/')
def home(lang):
    """Exibe a página inicial."""
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('home', lang=DEFAULT_LANGUAGE))
    
    site_config = ConfiguracaoSite.query.first()
    return render_with_lang('index.html', site_config=site_config)

# --- ROTA SEPARADA PARA A LISTA DE ROTEIROS ---
@app.route('/<string:lang>/roteiros')
def roteiros_lista(lang):
    """Exibe a página com a LISTA de todos os roteiros."""
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('roteiros_lista', lang=DEFAULT_LANGUAGE))
    
    # Aqui você renderiza a página que mostra todos os cards de roteiros
    # No futuro, você pode passar a lista completa de roteiros para o template
    return render_with_lang('roteiros.html', todos_roteiros=DADOS_ROTEIROS)


# --- ROTA CORRIGIDA PARA OS DETALHES DE UM ROTEIRO ---
@app.route('/<string:lang>/roteiros/<string:roteiro_slug>')
def roteiro_detalhe(lang, roteiro_slug):
    """Exibe a página de DETALHES de um roteiro específico."""
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('roteiro_detalhe', lang=DEFAULT_LANGUAGE, roteiro_slug=roteiro_slug))

    # Busca o roteiro específico no nosso dicionário de dados
    roteiro = DADOS_ROTEIROS.get(roteiro_slug)

    # Se o roteiro não for encontrado, exibe um erro 404
    if not roteiro:
        # Idealmente, você teria um template '404.html'
        return "Roteiro não encontrado", 404

    # Renderiza a página de detalhes, passando os dados do roteiro encontrado
    return render_with_lang('roteiro_detalhe.html', roteiro=roteiro)


# --- Demais Rotas ---

@app.route('/<string:lang>/blog')
def blog(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('blog', lang=DEFAULT_LANGUAGE))
    return render_with_lang('blog.html')

@app.route('/<string:lang>/destinos')
def destinations(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('destinations', lang=DEFAULT_LANGUAGE))
    return render_with_lang('destinos.html')

@app.route('/<string:lang>/comunidade')
def community(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('community', lang=DEFAULT_LANGUAGE))
    return render_with_lang('comunidade.html')

@app.route('/<string:lang>/loja')
def shop(lang):
    # Correção do bug de digitação
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('shop', lang=DEFAULT_LANGUAGE))
    return render_with_lang('loja.html')

@app.route('/<string:lang>/perfil')
def profile(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('profile', lang=DEFAULT_LANGUAGE))
    return render_with_lang('perfil.html')

@app.route('/<string:lang>/planos')
def plans(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(url_for('plans', lang=DEFAULT_LANGUAGE))
    return render_with_lang('planos.html')

# --- ROTA CORRIGIDA PARA MUDANÇA DE IDIOMA ---
@app.route('/change-language/<string:new_lang>')
def change_language(new_lang):
    if new_lang not in SUPPORTED_LANGUAGES:
        new_lang = DEFAULT_LANGUAGE
    session['lang'] = new_lang

    # Tenta de forma inteligente voltar para a página anterior com o novo idioma
    referer = request.headers.get('Referer')
    if referer:
        # Substitui o código de idioma antigo pelo novo na URL anterior
        from urllib.parse import urlparse
        old_path = urlparse(referer).path
        path_parts = old_path.split('/')
        if len(path_parts) > 1 and path_parts[1] in SUPPORTED_LANGUAGES:
            path_parts[1] = new_lang
            new_path = '/'.join(path_parts)
            return redirect(new_path)
            
    # Caso não consiga, redireciona para a home no novo idioma
    return redirect(url_for('home', lang=new_lang))


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
