from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('Estoque/', v.estoque, name='estoque'),
    path('Contribuidores/', v.contribuidor, name='contribuidores'),
    path('Produtos/', v.produtos, name='produtos'),

    # # # CREATE
    path('Cadastrar Produto/', v.produto_Create, name='ProdutoForm'),
    path('Categoria/', v.categoria_Create, name='CategoriaForm'),
    path('Cadastrar Contribuidor/', v.contribuidor_Create, name='ContribuidorForm'),

    # MOVIMENTO DO PRODUTO
    path('Movimentar Produto/<slug:slug>/', v.movimento, name='Movimento_produto'),

    # # # READ
    path('Produto/Info: <slug:slug>/', v.produto_Read, name='Produto_read'),
    path('Categoria/Info: <slug:slug>/', v.categoria_Read, name='Categoria_read'),
    path('Contribuidor/Info: <slug:slug>/', v.contribuidor_Read, name='Contribuidor_read'),

    # MOVIMENTOS LIST
    path('Movimentos/', v.movimento_list, name='Movimento_list'),

    # # # UPDATE
    path('Produto/Editar: <slug:slug>/', v.produto_Update, name='Produto_update'),
    path('Categoria/Editar: <slug:slug>/', v.categoria_Update, name='Categoria_update'),
    path('Contribuidor/Editar: <slug:slug>/', v.contribuidor_Update, name='Contribuidor_update'),

    # # # DELETE
    path('Produto/Deletar: <slug:slug>/', v.produto_Delete, name='Produto_delete'),
    path('Categoria/Deletar: <slug:slug>/', v.categoria_Delete, name='Categoria_delete'),
    path('Contribuidor/Deletar: <slug:slug>/', v.contribuidor_Delete, name='Contribuidor_delete'),
    

    
]