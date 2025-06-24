import i18n
import json
import os

# Caminho para o seu arquivo translations.json
# Certifique-se de que este caminho está correto em relação ao local onde você executa seu script.
# Se translations.json estiver na mesma pasta:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSLATIONS_FILE = os.path.join(BASE_DIR, 'translations.json')

# Carrega as traduções do arquivo JSON
try:
    with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
        all_translations = json.load(f)
except FileNotFoundError:
    print(f"Erro: O arquivo de traduções '{TRANSLATIONS_FILE}' não foi encontrado.")
    all_translations = {} # Garante que a variável seja definida
except json.JSONDecodeError:
    print(f"Erro: O arquivo '{TRANSLATIONS_FILE}' não é um JSON válido.")
    all_translations = {}

def configure_i18n():
    # Define o idioma padrão (fallback)
    i18n.set('fallback', 'pt') # Português como padrão

    # Carrega os recursos de tradução
    # O pacote i18n espera um dicionário onde a chave é o código do idioma
    # e o valor é outro dicionário com as chaves de tradução.
    # Seu translations.json já está nesse formato, ótimo!
    i18n.load_path.append(os.path.dirname(TRANSLATIONS_FILE)) # Não é estritamente necessário se você carregar tudo de uma vez
                                                                # mas pode ser útil para estruturar futuramente.

    # Adiciona as traduções carregadas diretamente ao i18n
    for lang_code, messages in all_translations.items():
        i18n.add_translation(lang_code, messages)

    # Opcional: configurar o detector de idioma (ex: baseado em variável de ambiente)
    # i18n.set('locale', os.environ.get('LANG', 'pt').split('_')[0])
    # Ou você pode definir manualmente em algum ponto da sua aplicação:
    i18n.set('locale', 'pt') # Define o idioma inicial para 'pt'

# Chama a função de configuração ao importar o módulo
configure_i18n()

# A função de tradução será acessível como i18n.t()
# Exemplo de como você usaria:
# from i18n_config import i18n
# print(i18n.t('site_name'))
