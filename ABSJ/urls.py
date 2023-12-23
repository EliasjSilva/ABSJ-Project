from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('Estoque/', v.estoque, name='estoque'),
    path('Contribuidores/', v.contribuidor, name='contribuidores'),
    path('Produtos/', v.produtos, name='produtos'),

    # # # CREATE
    path('Cadastrar Produto/', v.produto_Create, name='ProdutoForm'),
    path('Cadastrar Categoria/', v.category_Create, name='CategoriaForm'),
    path('Cadastrar Contribuidor/', v.contribuidor_Create, name='ContribuidorForm'),

    # MOVIMENTO DO PRODUTO
    path('Movimentar Produto/<int:id>/', v.movimento, name='Movimento_produto'),

    # # # READ
    path('Produto/<int:id>/', v.produto_Read, name='Produto_read'),
    path('Categoria/<int:id>/', v.category_Read, name='Categoria_read'),
    path('Contribuidor/<int:id>/', v.contribuidor_Read, name='Contribuidor_read'),

    # # # UPDATE
    path('Editar Produto/<int:id>/', v.produto_Update, name='Produto_update'),
    path('Editar Categoria/<int:id>/', v.category_Update, name='Categoria_update'),
    path('Editar Contribuidor/<int:id>/', v.contribuidor_Update, name='Contribuidor_update'),

    # # # DELETE
    path('Deletar Produto/<int:id>/', v.produto_Delete, name='Produto_delete'),
    path('Deletar Categoria/<int:id>/', v.categoria_Delete, name='Categoria_delete'),
    path('Deletar Contribuidor/<int:id>/', v.contribuidor_Delete, name='Contribuidor_delete'),
    

    
]