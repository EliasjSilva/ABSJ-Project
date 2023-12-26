from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m, forms as f
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from unidecode import unidecode
from django.db.models import Q





def home(request):
    return render(request, 'home.html')


def estoque(request):
    produtos = m.Produto.objects.all()
    categorias = m.Categoria.objects.all()
    contribuidores = m.Contribuidor.objects.all()

    # Buscador
    busca = request.GET.get('busca')
    categoria_id = request.GET.get('categoria')
    contribuidor_id = request.GET.get('contribuidor')

    if busca:
        try:
            busca_int = int(busca)
            produtos = produtos.filter(
                Q(codigo__icontains=busca),
            )
        except ValueError:
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

@login_required
def produtos(request):
    produto_list = m.Produto.objects.all()

    busca = request.GET.get('busca')
    if busca:

        # Quando for pesquisar tentar por inteiro, se der erro tenta o outro :p
        try:
            busca_int = int(busca)
            produto_list = produto_list.filter(
                Q(codigo__icontains=busca_int)
            )
        except ValueError:
            produto_list = produto_list.filter(
                Q(produto__icontains=busca) | Q(produto__icontains=unidecode(busca))
                )

    return render (request, 'list_Produtos.html', {'produtos':produto_list})


@login_required
def movimento_list(request):
    movimentos = m.Movimento.objects.all()

    tipo = request.GET.get('tipo')

    if tipo:
        movimentos = movimentos.filter(tipo=tipo)

    return render(request, 'list_Movimento.html', {'movimentos':movimentos})




# # # CREATING

@login_required
def produto_Create(request):
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None, user=request.user)

    if produtoForm.is_valid():
        produtoForm = produtoForm.save(commit=False)
        produtoForm.save()

        messages.info(request, f'Produto {produtoForm.produto} cadastrado com Sucesso!')
        return redirect('ProdutoForm')
    else:
        return render(request, 'create_Produto.html', {'formPro':produtoForm})

@login_required
def categoria_Create(request):
    categoriaForm = f.CategoriaForm(request.POST or None, request.FILES or None, user=request.user)
    categorias = m.Categoria.objects.all()

    if categoriaForm.is_valid():
        categoriaForm = categoriaForm.save(commit=False)
        categoriaForm.save()

        messages.info(request, f'Categoria {categoriaForm.categoria} adicionada com êxito!')
        return redirect('CategoriaForm')
    else:
        return render(request, 'create_Categoria.html', {'formCat':categoriaForm, 'categorias':categorias})

@login_required
def contribuidor_Create(request):
    contribForm = f.ContribuidorForm(request.POST or None, request.FILES or None, user=request.user)
    contribuidores = m.Contribuidor.objects.all()

    if contribForm.is_valid():
        contribForm = contribForm.save(commit=False)
        contribForm.save()

        messages.info(request, f'Contribuidor {contribForm.contribuidor} adicionado com êxito!')
        return redirect('ContribuidorForm')
    else:
        return render(request, 'create_Contribuidor.html', {'formCon':contribForm, 'contribuidores':contribuidores})


    # MOVIMENTAÇÃO DE PRODUTOS
@login_required
def movimento(request, id):
    produto = m.Produto.objects.get(id=id)

    if request.method == 'POST':

        # Instanciando o user e o produto para já estar selecionado quando for entrar na página //  Por algum motivo não funcionou como na view produto_Create
        produto_movimento = f.MovimentoForm(request.POST, request.FILES, initial={'user':request.user, 'produto':produto})
        if produto_movimento.is_valid():
            quantidade = produto_movimento.cleaned_data['quantidade']
            tipo = produto_movimento.cleaned_data['tipo']

            if tipo == 'Entrada':
                messages.info(request, f'Entrando +{quantidade} ao Produto: {produto.produto}')


            elif tipo == 'Saída':
                messages.info(request, f'Saindo -{quantidade} ao Produto: {produto.produto}')

            produto.save()
            m.Movimento.objects.create(produto=produto, quantidade=quantidade, tipo=tipo, user=request.user)
            return redirect('produtos')
    else:
        produto_movimento = f.MovimentoForm( initial={'user':request.user, 'produto':produto})
    
    return render(request, 'movimeto_produtos.html', {'movimento': produto_movimento, 'produto':produto})




# # # READING

@login_required
def produto_Read(request, id):
    read_produto = m.Produto.objects.get(id=id)
    
    # Verifica se a última atualização foi feita hoje
    if read_produto.tempo_ultima_atualizacao != date.today():
        # Se não foi atualizado hoje, realiza as atualizações
        read_produto.salvar_alteracoes()
        read_produto.tempo_ultima_atualizacao = date.today()
        read_produto.save()

    # Calcula o tempo de contribuição
    validade_dias = read_produto.calcular_tempo_validade()

    return render(request, 'read_Produto.html', {'readPro':read_produto, 'validade_dias':validade_dias})

@login_required
def contribuidor_Read(request, id):
    read_Contribuidor = m.Contribuidor.objects.get(id=id) 

    # Verifica se a última atualização foi feita hoje
    if read_Contribuidor.tempo_ultima_atualizacao != date.today():
        # Se não foi atualizado hoje, realiza as atualizações
        read_Contribuidor.salvar_alteracoes()
        read_Contribuidor.tempo_ultima_atualizacao = date.today()
        read_Contribuidor.save()

    # Calcula o tempo de contribuição
    dias_contribuicao = read_Contribuidor.calcular_tempo_contribuicao()

    return render(request, 'read_Contribuidor.html', {'readCon':read_Contribuidor, 'dias_contribuicao': dias_contribuicao})

@login_required
def categoria_Read(request, id):
    read_Cateogria = m.Categoria.objects.get(id=id)
    return render(request, 'read_Categoria.html', {'readCat':read_Cateogria})



# # # UPDATING
@login_required
def produto_Update(request, id):
    update_produto = m.Produto.objects.get(id=id)

    if request.method == 'POST':
        produtoEdit = f.ProdutoForm(request.POST, request.FILES, instance=update_produto)
        if produtoEdit.is_valid():
            produtoEdit = produtoEdit.save(commit=False)
            produtoEdit.save()

            messages.info(request, f'Produto {produtoEdit} Editado!')
            return redirect('Produto_read', id=update_produto.id)
    else:
        produtoEdit = f.ProdutoForm(instance=update_produto)

    return render(request, 'create_Produto.html', {'formPro': produtoEdit})
    
@login_required
def categoria_Update(request, id):
    update_categoria = m.Categoria.objects.get(id=id)
    categorias = m.Categoria.objects.all()

    if request.method == 'POST':
        categoriaEdit = f.CategoriaForm(request.POST, request.FILES, instance=update_categoria)
        if categoriaEdit.is_valid():
            categoriaEdit = categoriaEdit.save(commit=False)
            categoriaEdit.save()

            messages.info(request, f'Categoria {categoriaEdit} Editado!')
            return redirect('Categoria_read', id=update_categoria.id)
    else:
        categoriaEdit = f.CategoriaForm(instance=update_categoria)

    return render(request, 'create_Categoria.html', {'formCat': categoriaEdit, 'categorias':categorias})
    
@login_required
def contribuidor_Update(request, id):
    update_contribuidor = m.Contribuidor.objects.get(id=id)

    if request.method == 'POST':
        contribuidorEdit = f.ContribuidorForm(request.POST, request.FILES, instance=update_contribuidor)
        if contribuidorEdit.is_valid():
            contribuidorEdit = contribuidorEdit.save(commit=False)
            contribuidorEdit.save()

            messages.info(request, f'Contribuidor {contribuidorEdit} Editado!')
            return redirect('Contribuidor_read', id=update_contribuidor.id)
    else:
        contribuidorEdit = f.ContribuidorForm(instance=update_contribuidor)

    return render(request, 'create_Contribuidor.html', {'formCon': contribuidorEdit})




# # # DELETING

@login_required
def produto_Delete(request, id):
    delete_produto = m.Produto.objects.get(id=id)
    delete_produto.delete()

    messages.info(request, f'Produto {delete_produto.produto} Excluido!')
    return redirect('produtos')


@login_required
def categoria_Delete(request, id):
    delete_categoria = m.Categoria.objects.get(id=id)
    delete_categoria.delete()

    messages.info(request, f'Categoria {delete_categoria.categoria} Excluido!')
    return redirect('CategoriaForm')


@login_required
def contribuidor_Delete(request, id):
    delete_contribuidor = m.Contribuidor.objects.get(id=id)
    delete_contribuidor.delete()

    messages.info(request, f'Contribuidor {delete_contribuidor.contribuidor} Excluido!')
    return redirect('contribuidores')
