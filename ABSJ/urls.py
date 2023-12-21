from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('Estoque/', v.estoque, name='estoque'),
    path('Fornecedores/', v.fornecedor, name='fornecedor'),

    # # # CREATE
    path('Cadastrar Produto/', v.produto_Create, name='ProdutoForm'),
    path('Cadastrar Categoria/', v.category_Create, name='CategoryForm'),
    path('Cadastrar Fornercedor/', v.fornercedor_Create, name='FornercedorForm'),

    # # # READ
    path('Produto/<int:id>/', v.produto_Read, name='Produto_read'),
    path('Category/<int:id>/', v.category_Read, name='Category_read'),
    path('Contribuidor/<int:id>/', v.contribuidor_Read, name='Contribuidor_read'),

    # # # UPDATE
    

    
]