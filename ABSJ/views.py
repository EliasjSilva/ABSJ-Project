from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m, forms as f
from django.contrib.auth.decorators import login_required
from datetime import datetime
from unidecode import unidecode
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def produtos(request):
    produto_list = m.Produto.objects.all()

    busca = request.GET.get('busca')
    if busca:
        produto_list = produto_list.filter(
            Q(produto__icontains=busca) | Q(produto__icontains=unidecode(busca))
            )

    return render (request, 'list_Produtos.html', {'produtos':produto_list})


def estoque(request):

    produtos = m.Produto.objects.all()
    categorias = m.Categoria.objects.all()
    contribuidores = m.Contribuidor.objects.all()

    # Buscador
    busca = request.GET.get('busca')
    categoria_id = request.GET.get('categoria')
    contribuidor_id = request.GET.get('contribuidor')

    if busca:
        produtos = produtos.filter(
            Q(produto__icontains=busca) | Q(produto__icontains=unidecode(busca))
            )

    if categoria_id:
        produtos = produtos.filter(categoria__id=categoria_id)
    if contribuidor_id:
        produtos = produtos.filter(contribuidor__id=contribuidor_id)

    return render (request, 'list_Estoque.html', {'produtos':produtos, 'categorias':categorias, 'contribuidores':contribuidores})


@login_required
def contribuidor(request):
    contribuidores = m.Contribuidor.objects.all()
    return render (request, 'list_Contribuidores.html', {'contribuidores':contribuidores})




# # # CREATING

@login_required
def produto_Create(request):
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None, user=request.user)

    if produtoForm.is_valid():
        produtoForm = produtoForm.save(commit=False)
        produtoForm.save()

        messages.info(request, f'Produto {produtoForm.produto} cadastrado com Sucesso!')
        return redirect('estoque')
    else:
        return render(request, 'create_Produto.html', {'formPro':produtoForm})

@login_required
def category_Create(request):
    categoriaForm = f.CategoriaForm(request.POST or None, request.FILES or None, user=request.user)
    categorias = m.Categoria.objects.all()

    if categoriaForm.is_valid():
        categoriaForm = categoriaForm.save(commit=False)
        categoriaForm.save()

        messages.info(request, f'Categoria {categoriaForm.categoria} adicionada com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Categoria.html', {'formCat':categoriaForm, 'categorias':categorias})

@login_required
def contribuidor_Create(request):
    contribForm = f.ContribuidorForm(request.POST or None, request.FILES or None, user=request.user)

    if contribForm.is_valid():
        contribForm = contribForm.save(commit=False)
        contribForm.save()

        messages.info(request, f'Contribuidor {contribForm.contribuidor} adicionado com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Contribuidor.html', {'formCon':contribForm})




    # # # MOVIMENTAÇÃO DE PRODUTOS
def movimento(request, id):
    produto = m.Produto.objects.get(id=id)

    if request.method == 'POST':

        # Instanciando o user e o produto para já estar selecionado quando for entrar na página //  Por algum motivo não funcionou como na view produto_Create
        produto_movimento = f.MovimentoForm(request.POST, request.FILES, initial={'user':request.user, 'produto':produto})
        if produto_movimento.is_valid():
            quantidade = produto_movimento.cleaned_data['quantidade']
            tipo = produto_movimento.cleaned_data['tipo']

            if tipo == 'Entrada':
                produto.estoque += quantidade
                messages.info(request, f'Entrando +{quantidade} ao Produto: {produto.produto}')


            elif tipo == 'Saída':
                produto.estoque -= quantidade
                messages.info(request, f'Saindo -{quantidade} ao Produto: {produto.produto}')

                if produto.estoque < 0:
                    produto.estoque = 0

            produto.save()
            m.Movimento.objects.create(produto=produto, quantidade=quantidade, tipo=tipo, user=request.user)
            return redirect('estoque')
    else:
        produto_movimento = f.MovimentoForm( initial={'user':request.user, 'produto':produto})
    
    return render(request, 'movimeto_produtos.html', {'movimento': produto_movimento, 'produto':produto})


# # # READING

@login_required
def produto_Read(request, id):
    read_produto = m.Produto.objects.get(id=id)
    return render(request, 'read_Produto.html', {'readPro':read_produto})

@login_required
def contribuidor_Read(request, id):
    read_Contribuidor = m.Contribuidor.objects.get(id=id)

    return render(request, 'read_Contribuidor.html', {'readCon':read_Contribuidor})

@login_required
def category_Read(request, id):
    read_Cateogry = m.Categoria.objects.get(id=id)
    return render(request, 'read_Categoria.html', {'readCat':read_Cateogry})




# # # UPDATING
def produto_Update(request, id):
    update_produto = m.Produto.objects.get(id=id)

    if request.method == 'POST':
        produtoEdit = f.ProdutoForm(request.POST, request.FILES, instance=update_produto)
        if produtoEdit.is_valid():
            produtoEdit = produtoEdit.save(commit=False)
            produtoEdit.save()

            messages.info(request, f'Produto {produtoEdit} Editado!')
            return redirect('estoque')
    else:
        produtoEdit = f.ProdutoForm(instance=update_produto)

    return render(request, 'create_Produto.html', {'formPro': produtoEdit})
    
def category_Update(request, id):
    update_category = m.Categoria.objects.get(id=id)
    categorias = m.Categoria.objects.all()

    if request.method == 'POST':
        categoryEdit = f.CategoriaForm(request.POST, request.FILES, instance=update_category)
        if categoryEdit.is_valid():
            categoryEdit = categoryEdit.save(commit=False)
            categoryEdit.save()

            messages.info(request, f'Categoria {categoryEdit} Editado!')
            return redirect('estoque')
    else:
        categoryEdit = f.CategoriaForm(instance=update_category)

    return render(request, 'create_Categoria.html', {'formCat': categoryEdit, 'categorias':categorias})
    
def contribuidor_Update(request, id):
    update_contribuidor = m.Contribuidor.objects.get(id=id)

    if request.method == 'POST':
        contribuidorEdit = f.ContribuidorForm(request.POST, request.FILES, instance=update_contribuidor)
        if contribuidorEdit.is_valid():
            contribuidorEdit = contribuidorEdit.save(commit=False)
            contribuidorEdit.save()

            messages.info(request, f'Contribuidor {contribuidorEdit} Editado!')
            return redirect('estoque')
    else:
        contribuidorEdit = f.ContribuidorForm(instance=update_contribuidor)

    return render(request, 'create_Contribuidor.html', {'formCon': contribuidorEdit})




# # # DELETING

def produto_Delete(request, id):
    delete_produto = m.Produto.objects.get(id=id)
    delete_produto.delete()

    messages.info(request, f'Produto {delete_produto.produto} Excluido!')
    return redirect('estoque')

def categoria_Delete(request, id):
    delete_categoria = m.Categoria.objects.get(id=id)
    delete_categoria.delete()

    messages.info(request, f'Categoria {delete_categoria.categoria} Excluido!')
    return redirect('estoque')

def contribuidor_Delete(request, id):
    delete_contribuidor = m.Contribuidor.objects.get(id=id)
    delete_contribuidor.delete()

    messages.info(request, f'Contribuidor {delete_contribuidor.contribuidor} Excluido!')
    return redirect('estoque')
