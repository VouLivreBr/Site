# Documentação do Site Vou Livre

## Visão Geral

O Vou Livre é um site de guia de viagens focado inicialmente no Rio de Janeiro, com planos de expansão para outros destinos no Brasil e no mundo. O site oferece roteiros de viagem, informações sobre destinos, blog com dicas, comunidade para viajantes e uma loja para compra de roteiros premium.

## Estrutura do Projeto

```
vou_livre_site/
├── src/
│   ├── main.py                 # Arquivo principal do Flask
│   ├── models/                 # Modelos de dados
│   ├── routes/                 # Rotas da aplicação
│   ├── static/                 # Arquivos estáticos
│   │   ├── css/                # Estilos CSS
│   │   ├── images/             # Imagens
│   │   │   └── flags/          # Bandeiras para seletor de idiomas
│   │   └── js/                 # Scripts JavaScript
│   └── templates/              # Templates HTML
│       ├── base_multilingual.html  # Template base com suporte multilíngue
│       ├── index.html          # Página inicial
│       ├── roteiros.html       # Página de roteiros
│       ├── blog.html           # Página de blog
│       └── ...                 # Outras páginas
├── venv/                       # Ambiente virtual Python
└── requirements.txt            # Dependências do projeto
```

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / MySQL (produção)
- **Responsividade**: Design responsivo para dispositivos móveis e desktop
- **Multilíngue**: Suporte para português, inglês e espanhol

## Funcionalidades Principais

### 1. Sistema Multilíngue
- Suporte completo para português, inglês e espanhol
- Seletor de idiomas no cabeçalho
- Detecção automática do idioma do navegador
- Arquivos de tradução em formato JSON

### 2. Roteiros de Viagem
- Modelo freemium: um roteiro gratuito de 1 dia e roteiros premium pagos
- Sistema de filtros por destino, duração, tipo e preço
- Ordenação por relevância, preço e avaliação
- Detalhes completos dos roteiros com mapas interativos

### 3. Blog
- Artigos sobre dicas de viagem, atrações, gastronomia, etc.
- Categorização por temas
- Sistema de busca e filtros
- Comentários e compartilhamento

### 4. Comunidade
- Feed de publicações de usuários
- Perfis de viajantes
- Sistema de seguir outros usuários
- Compartilhamento de experiências e fotos

### 5. Loja (E-commerce)
- Venda de roteiros premium
- Sistema de assinatura (mensal, semestral, anual)
- Processamento de pagamentos
- Área de membros para acesso ao conteúdo premium

### 6. Sistema de Usuários
- Cadastro e login
- Perfil personalizado
- Histórico de viagens
- Roteiros salvos e favoritos

## Guia de Instalação

### Requisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Passos para Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/vou-livre-site.git
cd vou-livre-site
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
export FLASK_APP=src/main.py
export FLASK_ENV=development
```

5. Inicie o servidor de desenvolvimento:
```bash
flask run
```

6. Acesse o site em `http://localhost:5000`

## Guia de Manutenção

### Adicionando Novos Idiomas

1. Crie um novo arquivo de tradução em `src/static/translations.json`
2. Adicione o novo idioma ao array `SUPPORTED_LANGUAGES` em `src/main.py`
3. Adicione a bandeira do idioma em `src/static/images/flags/`
4. Adicione a opção no seletor de idiomas em `src/templates/base_multilingual.html`

### Adicionando Novos Roteiros

1. Crie um novo registro no banco de dados com as informações do roteiro
2. Adicione imagens relacionadas em `src/static/images/roteiros/`
3. Crie um template para o detalhe do roteiro em `src/templates/roteiro_detalhe.html`

### Adicionando Novos Destinos

1. Crie um novo registro no banco de dados com as informações do destino
2. Adicione imagens relacionadas em `src/static/images/destinos/`
3. Crie um template para o detalhe do destino em `src/templates/destino_detalhe.html`

## Publicação

### Preparação para Produção

1. Atualize o arquivo `requirements.txt`:
```bash
pip freeze > requirements.txt
```

2. Configure as variáveis de ambiente para produção:
```bash
export FLASK_ENV=production
export DATABASE_URL=mysql://usuario:senha@host:porta/banco
```

3. Configure o servidor web (Nginx, Apache) para servir a aplicação Flask

### Hospedagem Recomendada

- **Opções de hospedagem**: Heroku, AWS, DigitalOcean, PythonAnywhere
- **Domínio recomendado**: voulivre.com.br

## Modelo de Monetização

O site Vou Livre utiliza um modelo de monetização freemium:

1. **Conteúdo Gratuito**:
   - Roteiro de 1 dia para o Rio de Janeiro
   - Informações básicas sobre destinos
   - Artigos do blog
   - Perfil básico na comunidade

2. **Conteúdo Premium (Pago)**:
   - Roteiros completos de 2+ dias
   - Mapas interativos detalhados
   - Dicas exclusivas
   - Descontos com parceiros

3. **Planos de Assinatura**:
   - Mensal: R$ 29,90/mês
   - Semestral: R$ 149,90/6 meses (economia de 16%)
   - Anual: R$ 249,90/ano (economia de 30%)

## Contato e Suporte

Para suporte técnico ou dúvidas sobre o site, entre em contato:

- **Email**: suporte@voulivre.com.br
- **Telefone**: (XX) XXXX-XXXX

---

Documentação criada em: Maio de 2025
