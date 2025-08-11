# E-Shop Brasil - Projeto de Banco de Dados e Big Data (MongoDB + Streamlit + Docker)

**Resumo:** Projeto prático para disciplina *Advanced Databases and Big Data*. Implementa uma pequena aplicação em Streamlit que conecta a um MongoDB rodando em Docker, permitindo inserir, editar, excluir e consultar produtos e pedidos. Inclui `docker-compose` para orquestrar serviços e um script para popular o banco com dados de exemplo.

## Estrutura do repositório
```
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── seed_db.py
├── seed_data.json
└── .gitignore
```

## Como rodar (modo simples)
1. Clone o repositório:
```bash
git clone <seu-repo>
cd eshop_project
```

2. Subir tudo com Docker Compose (vai buildar a imagem da aplicação):
```bash
docker-compose up --build
```
- O MongoDB ficará disponível em `mongodb://mongo:27017/`
- A aplicação Streamlit estará disponível em `http://localhost:8501`

3. Popular o banco (opcional):
```bash
# Em outro terminal, após mongo subir:
docker-compose run --rm seed
```
Isso executa `seed_db.py` e insere dados de exemplo na base `eshop` nas coleções `products` e `orders`.

## Alternativa - rodando localmente (sem Docker)
1. Crie um virtualenv e instale dependências:
```bash
python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate    # windows
pip install -r requirements.txt
```
2. Configure a variável `MONGO_URI` (ex.: `mongodb://localhost:27017/eshop`)
3. Execute:
```bash
streamlit run app.py
```

## O que a aplicação faz
- Conectar ao MongoDB (URI pela variável de ambiente `MONGO_URI`, por padrão `mongodb://mongo:27017/eshop`)
- Inserir produtos (nome, sku, category, price, stock)
- Editar e remover produtos
- Listar produtos com filtros
- Inserir pedidos simples (cliente, items, total, status)
- Relatórios básicos (contagem por categoria, produtos sem estoque)

## Observações
- Projeto simples para fins acadêmicos. Não use em produção sem adicionar autenticação, validação completa e políticas de segurança (LGPD).
- Para avaliação, deixe o repositório público e inclua prints/gifs em `exemplos/` se quiser demonstrar fluxo.
