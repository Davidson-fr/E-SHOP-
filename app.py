import os
import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId

st.set_page_config(page_title='E-Shop Brasil - Admin', layout='wide')

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/eshop')
client = MongoClient(MONGO_URI)
db = client.eshop

st.title('E-Shop Brasil - Painel de Admin (Exemplo)')

menu = st.sidebar.selectbox('Menu', ['Dashboard','Produtos','Pedidos','Config'])

if menu == 'Dashboard':
    st.header('Dashboard')
    col1, col2, col3 = st.columns(3)
    total_products = db.products.count_documents({})
    total_orders = db.orders.count_documents({})
    out_of_stock = db.products.count_documents({'stock': {'$lte': 0}})
    col1.metric('Produtos cadastrados', total_products)
    col2.metric('Pedidos registrados', total_orders)
    col3.metric('Produtos sem estoque', out_of_stock)

    st.subheader('Produtos por categoria')
    pipeline = [
        {'$group': {'_id': '$category', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    cat = list(db.products.aggregate(pipeline))
    if cat:
        dfc = pd.DataFrame(cat)
        dfc = dfc.rename(columns={'_id':'category'})
        st.table(dfc)
    else:
        st.write('Nenhum dado de produto encontrado.')

if menu == 'Produtos':
    st.header('Gerenciar Produtos')

    with st.expander('Cadastrar novo produto'):
        with st.form('add_product'):
            sku = st.text_input('SKU')
            name = st.text_input('Nome')
            category = st.text_input('Categoria')
            price = st.number_input('Preço', min_value=0.0, format='%.2f')
            stock = st.number_input('Estoque', min_value=0, step=1)
            submitted = st.form_submit_button('Salvar')
            if submitted:
                doc = {'sku': sku, 'name': name, 'category': category, 'price': float(price), 'stock': int(stock)}
                db.products.insert_one(doc)
                st.success('Produto inserido com sucesso.')

    st.subheader('Lista de produtos')
    q = st.text_input('Pesquisar por nome / sku / categoria')
    query = {}
    if q:
        query = {'$or': [
            {'name': {'$regex': q, '$options': 'i'}},
            {'sku': {'$regex': q, '$options': 'i'}},
            {'category': {'$regex': q, '$options': 'i'}}
        ]}
    cursor = db.products.find(query).limit(500)
    products = list(cursor)
    if products:
        df = pd.DataFrame(products)
        df = df.drop(columns=['_id']).rename(columns={'sku':'SKU','name':'Nome','category':'Categoria','price':'Preço','stock':'Estoque'})
        st.dataframe(df)
        sel = st.selectbox('Selecionar produto (por SKU) para editar/excluir', [''] + [p['sku'] for p in products])
        if sel:
            prod = db.products.find_one({'sku': sel})
            if prod:
                with st.form('edit_product'):
                    new_name = st.text_input('Nome', value=prod.get('name',''))
                    new_category = st.text_input('Categoria', value=prod.get('category',''))
                    new_price = st.number_input('Preço', value=float(prod.get('price',0.0)), format='%.2f')
                    new_stock = st.number_input('Estoque', value=int(prod.get('stock',0)))
                    save = st.form_submit_button('Salvar alterações')
                    delete = st.form_submit_button('Excluir produto')
                    if save:
                        db.products.update_one({'_id': prod['_id']}, {'$set': {'name': new_name, 'category': new_category, 'price': float(new_price), 'stock': int(new_stock)}})
                        st.success('Produto atualizado.')
                    if delete:
                        db.products.delete_one({'_id': prod['_id']})
                        st.success('Produto excluído.')

    else:
        st.info('Nenhum produto encontrado. Use o formulário acima para inserir.')

if menu == 'Pedidos':
    st.header('Pedidos (simplificado)')
    with st.expander('Criar pedido'):
        with st.form('add_order'):
            order_id = st.text_input('Order ID (ex: ORD-1003)')
            customer = st.text_input('Cliente')
            items_raw = st.text_area('Itens como JSON (ex: [{"sku":"WAVE-0001","qty":1,"price":1299.9}])')
            status = st.selectbox('Status', ['processing','shipped','delivered','cancelled'])
            submitted = st.form_submit_button('Criar pedido')
            if submitted:
                try:
                    items = eval(items_raw) if items_raw.strip() else []
                    total = sum([float(i.get('price',0))*int(i.get('qty',1)) for i in items])
                    doc = {'order_id': order_id, 'customer': customer, 'items': items, 'total': float(total), 'status': status}
                    db.orders.insert_one(doc)
                    st.success('Pedido criado.')
                except Exception as e:
                    st.error('Erro ao criar pedido: ' + str(e))

    st.subheader('Lista de pedidos')
    cursor = db.orders.find({}).limit(500)
    orders = list(cursor)
    if orders:
        df = pd.json_normalize(orders)
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
        st.dataframe(df)
    else:
        st.info('Nenhum pedido registrado.')

if menu == 'Config':
    st.header('Configurações')
    st.write('URI do MongoDB atual:')
    st.code(MONGO_URI)
    st.write('Observação: para ambientes de produção, use variáveis de ambiente e segredos para armazenar credenciais.')
