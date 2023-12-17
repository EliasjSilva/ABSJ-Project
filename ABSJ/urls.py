from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('Estoque/', v.estoque, name='estoque'),
    path('Fornecedores/', v.fornecedor, name='fornecedor'),


    path('Cadastrar Produto/', v.produto_Create, name='ProdutoForm'),
    path('Cadastrar Categoria/', v.category_Create, name='CategoryForm'),
    path('Cadastrar Fornercedor/', v.fornercedor_Create, name='FornercedorForm'),

    
]