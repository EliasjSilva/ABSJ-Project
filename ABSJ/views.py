from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m, forms as f
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from unidecode import unidecode
from django.db.models import Q
from django.utils import html, dateparse, timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage





def home(request):
    produtos = m.Produto.objects.all()

    notifica = []
    notifica_prazo = []
    notifica_vencido = []
    hoje = date.today()

    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            # strftime(%d/%m/%Y) mostra o formato da data, antes mostrava como YYYY/mm/dd. import do datetime
            message = html.format_html('<span class="error-var">{}</span> venceu na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_vencido.append((produto, message))
            notifica.append(produto)
        elif 0 < diferenca <= 7:
            message = html.format_html('<span class="error-var">{}</span> está prestes a vencer na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_prazo.append((produto, message))
            notifica.append(produto)

    return render(request, 'home.html', {'notifica':notifica, 'notifica_prazo':notifica_prazo, 'notifica_vencido':notifica_vencido})


def estoque(request):
    produtos = m.Produto.objects.all()
    categorias = m.Categoria.objects.all()
    contribuidores = m.Contribuidor.objects.all()

    # Buscadores
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

    # Notificações
    notifica = []
    notifica_prazo = []
    notifica_vencido = []
    hoje = date.today()

    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            # strftime(%d/%m/%Y) mostra o formato da data, antes mostrava como YYYY/mm/dd. import do datetime
            message = html.format_html('<span class="error-var">{}</span> venceu na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_vencido.append((produto, message))
            notifica.append(produto)
        elif 0 < diferenca <= 7:
            message = html.format_html('<span class="error-var">{}</span> está prestes a vencer na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_prazo.append((produto, message))
            notifica.append(produto)

    # list - Paginator
    paginator = Paginator(produtos, 30)
    page = request.GET.get('page')
    try:
        produtos = paginator.page(page)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        produtos = paginator.page(paginator.num_pages)

    # Passar os parâmetros de filtro para a páginação
    params = request.GET.copy()
    if 'page' in params:
        del params['page']

    produtos.filter_params = params.urlencode()

    return render (request, 'list_Estoque.html', {'notifica':notifica, 'notifica_prazo':notifica_prazo, 'notifica_vencido':notifica_vencido, 'produtos':produtos, 'categorias':categorias, 'contribuidores':contribuidores})



@login_required
def contribuidor(request):
    contribuidores = m.Contribuidor.objects.all()
    
    # list - Paginator
    paginator = Paginator(contribuidores, 10)
    page = request.GET.get('page')
    try:
        contribuidores = paginator.page(page)
    except PageNotAnInteger:
        contribuidores = paginator.page(1)
    except EmptyPage:
        contribuidores = paginator.page(paginator.num_pages)

    return render (request, 'list_Contribuidores.html', {'contribuidores':contribuidores})

@login_required
def produtos(request):
    produtos = m.Produto.objects.all()

    # Buscadores
    busca = request.GET.get('busca')
    sDate = request.GET.get('start_date')
    eDate = request.GET.get('end_date')
    
    notifica = []
    notifica_prazo = []
    notifica_vencido = []
    hoje = date.today()

    if busca:

        # Quando for pesquisar tentar por inteiro, se der erro tenta o outro :p
        try:
            busca_int = int(busca)
            produtos = produtos.filter(
                Q(codigo__icontains=busca_int)
            )
        except ValueError:
            produtos = produtos.filter(
                Q(produto__icontains=busca) | Q(produto__icontains=unidecode(busca))
                )
    if sDate and eDate:
        eDate = dateparse.parse_date(eDate) + timedelta(1)

        produtos = produtos.filter(validade__range=[sDate, eDate])
        paginator = Paginator(produtos, 30)
        page = request.GET.get('page')
        try:
            produtos = paginator.page(page)
        except PageNotAnInteger:
            produtos = paginator.page(1)
        except EmptyPage:
            produtos = paginator.page(paginator.num_pages)

        # Passar os parâmetros de filtro para a páginação
        params = request.GET.copy()
        if 'page' in params:
            del params['page']

        produtos.filter_params = params.urlencode()

                
    # Notificações
    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            # strftime(%d/%m/%Y) mostra o formato da data, antes mostrava como YYYY/mm/dd. import do datetime
            message = html.format_html('<span class="error-var">{}</span> venceu na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_vencido.append((produto, message))
            notifica.append(produto)
        elif 0 < diferenca <= 7:
            message = html.format_html('<span class="error-var">{}</span> está prestes a vencer na data {}!', produto.produto, produto.validade.strftime('%d/%m/%Y'))
            notifica_prazo.append((produto, message))
            notifica.append(produto)

    
    # list - Paginator
    paginator = Paginator(produtos, 30)
    page = request.GET.get('page')
    try:
        produtos = paginator.page(page)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        produtos = paginator.page(paginator.num_pages)

    return render (request, 'list_Produtos.html', {'notifica':notifica, 'notifica_prazo':notifica_prazo, 'notifica_vencido':notifica_vencido, 'produtos':produtos})


@login_required
def movimento_list(request):
    movimentos = m.Movimento.objects.all()

    # Buscadores
    tipo = request.GET.get('tipo')
    sDate = request.GET.get('start_date')
    eDate = request.GET.get('end_date')

    if tipo:
        movimentos = movimentos.filter(tipo=tipo)
    
    if sDate and eDate:

        # Convertendo as strings em objetos datetime.date usando parse_date
        sDate = dateparse.parse_date(sDate)
        eDate = dateparse.parse_date(eDate) + timedelta(1)

        movimentos = movimentos.filter(modificado__range=[sDate, eDate])
        paginator = Paginator(movimentos, 30)
        page = request.GET.get('page')
        try:
            movimentos = paginator.page(page)
        except PageNotAnInteger:
            movimentos = paginator.page(1)
        except EmptyPage:
            movimentos = paginator.page(paginator.num_pages)

        # Passar os parâmetros de filtro para a páginação
        params = request.GET.copy()
        if 'page' in params:
            del params['page']

        movimentos.filter_params = params.urlencode()

    # list - Paginator
    paginator = Paginator(movimentos, 30)
    page = request.GET.get('page')
    try:
        movimentos = paginator.page(page)
    except PageNotAnInteger:
        movimentos = paginator.page(1)
    except EmptyPage:
        movimentos = paginator.page(paginator.num_pages)

    return render(request, 'list_Movimento.html', {'movimentos':movimentos})




# # # CREATING

@login_required
def produto_Create(request):
    produtos = m.Produto.objects.all()
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None, user=request.user)

    # Notificações
    venceu = []
    prazo = []
    hoje = date.today()

    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            venceu.append(produto)
        elif 0 < diferenca <= 7:
            prazo.append(produto)

    if produtoForm.is_valid():
        produtoForm = produtoForm.save(commit=False)
        produtoForm.save()

        messages.info(request, f'Produto {produtoForm.produto} cadastrado com Sucesso!')
        return redirect('ProdutoForm')
    else:
        return render(request, 'create_Produto.html', {'venceu':venceu, 'prazo':prazo, 'formPro':produtoForm, 'produtos':produtos})

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
def movimento(request, slug):
    produto = m.Produto.objects.get(slug=slug)

    if request.method == 'POST':

        # Instanciando o user e o produto para já estar selecionado quando for entrar na página //  Por algum motivo não funcionou como na view produto_Create
        produto_movimento = f.MovimentoForm(request.POST or None, request.FILES or None, initial={'user':request.user, 'produto':produto})
        if produto_movimento.is_valid():
            quantidade = produto_movimento.cleaned_data['quantidade']
            tipo = produto_movimento.cleaned_data['tipo']

            if tipo == 'Entrada':
                messages.info(request, f'Entrando +{quantidade} ao Produto: {produto}')


            elif tipo == 'Saída':
                messages.info(request, f'Saindo -{quantidade} ao Produto: {produto}')

            produto.save()
            m.Movimento.objects.create(produto=produto, quantidade=quantidade, tipo=tipo, user=request.user)
            return redirect('produtos')
    else:
        produto_movimento = f.MovimentoForm( initial={'user':request.user, 'produto':produto})
    
    return render(request, 'movimeto_produtos.html', {'movimento': produto_movimento, 'produto':produto})




# # # READING

@login_required
def produto_Read(request, slug):
    read_produto = m.Produto.objects.get(slug=slug)
    
    #filtra o  produto da página para listar os movimentos realacionados.
    movimentos = m.Movimento.objects.filter(produto=read_produto)
    
    # Verifica se a última atualização foi feita hoje
    if read_produto.tempo_ultima_atualizacao != date.today():
        # Se não foi atualizado hoje, realiza as atualizações
        read_produto.salvar_alteracoes()
        read_produto.tempo_ultima_atualizacao = date.today()
        read_produto.save()

    # Calcula o tempo de contribuição
    validade_dias = read_produto.calcular_tempo_validade()

    # Notificações
    notifica = []
    hoje = date.today()

    diferenca = (read_produto.validade - hoje).days

    if diferenca <= 0:
        notifica.append(read_produto)
    elif 0 < diferenca <= 7:
        notifica.append(read_produto)

    # list - Paginator
    paginator = Paginator(movimentos, 20)
    page = request.GET.get('page')
    try:
        movimentos = paginator.page(page)
    except PageNotAnInteger:
        movimentos = paginator.page(1)
    except EmptyPage:
        movimentos = paginator.page(paginator.num_pages)
    return render(request, 'read_Produto.html', {'validade_dias':validade_dias, 'notifica':notifica, 'movimentos':movimentos, 'readPro':read_produto})

@login_required
def contribuidor_Read(request, slug):
    read_Contribuidor = m.Contribuidor.objects.get(slug=slug) 
    produtos = m.Produto.objects.all()
    notifica = []
    hoje = date.today()

    # contar os produtos usando a função da models 'contar_produtos'
    quantidade_produtos = read_Contribuidor.contar_produtos()

    produtos_list = m.Produto.objects.filter(contribuidor=read_Contribuidor)

    # Verifica se a última atualização foi feita hoje
    if read_Contribuidor.tempo_ultima_atualizacao != date.today():
        # Se não foi atualizado hoje, realiza as atualizações
        read_Contribuidor.salvar_alteracoes()
        read_Contribuidor.tempo_ultima_atualizacao = date.today()
        read_Contribuidor.save()

    # Calcula o tempo de contribuição
    dias_contribuicao = read_Contribuidor.calcular_tempo_contribuicao()

    # Notificações
    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            notifica.append(produto)
        elif 0 < diferenca <= 7:
            notifica.append(produto)


    # list - Paginator
    paginator = Paginator(produtos_list, 20)
    page = request.GET.get('page')
    try:
        produtos_list = paginator.page(page)
    except PageNotAnInteger:
        produtos_list = paginator.page(1)
    except EmptyPage:
        produtos_list = paginator.page(paginator.num_pages)

    return render(request, 'read_Contribuidor.html', {'notifica':notifica, 'produtos_list':produtos_list, 'readCon':read_Contribuidor, 'dias_contribuicao': dias_contribuicao, 'quantidade_produtos':quantidade_produtos})

@login_required
def categoria_Read(request, slug):
    read_Cateogria = m.Categoria.objects.get(slug=slug)
    produtos_list = m.Produto.objects.filter(categoria=read_Cateogria)
    produtos = m.Produto.objects.all()

    # Notificações
    notifica = []
    hoje = date.today()

    for produto in produtos:
        diferenca = (produto.validade - hoje).days

        if diferenca <= 0:
            notifica.append(produto)
        elif 0 < diferenca <= 7:
            notifica.append(produto)

    # list - Paginator
    paginator = Paginator(produtos_list, 40)
    page = request.GET.get('page')
    try:
        produtos_list = paginator.page(page)
    except PageNotAnInteger:
        produtos_list = paginator.page(1)
    except EmptyPage:
        produtos_list = paginator.page(paginator.num_pages)

    return render(request, 'read_Categoria.html', {'notifica':notifica, 'produtos_list':produtos_list, 'readCat':read_Cateogria})



# # # UPDATING
@login_required
def produto_Update(request, slug):
    produtos = m.Produto.objects.all()
    update_produto = m.Produto.objects.get(slug=slug)

    if request.method == 'POST':
        produtoEdit = f.ProdutoForm(request.POST, request.FILES, instance=update_produto)
        if produtoEdit.is_valid():
            produtoEdit = produtoEdit.save(commit=False)
            produtoEdit.save()

            messages.info(request, f'Produto {produtoEdit.produto} foi Editado!')
            return redirect('Produto_read', slug=update_produto.slug)
    else:
        produtoEdit = f.ProdutoForm(instance=update_produto)

    return render(request, 'create_Produto.html', {'formPro': produtoEdit, 'produtos':produtos})
    
@login_required
def categoria_Update(request, slug):
    categorias = m.Categoria.objects.all()
    update_categoria = m.Categoria.objects.get(slug=slug)

    if request.method == 'POST':
        categoriaEdit = f.CategoriaForm(request.POST, request.FILES, instance=update_categoria)
        if categoriaEdit.is_valid():
            categoriaEdit = categoriaEdit.save(commit=False)
            categoriaEdit.save()

            messages.info(request, f'Categoria {categoriaEdit.categoria} foi Editado!')
            return redirect('Categoria_read', slug=update_categoria.slug)
    else:
        categoriaEdit = f.CategoriaForm(instance=update_categoria)

    return render(request, 'create_Categoria.html', {'formCat': categoriaEdit, 'categorias':categorias})
    
@login_required
def contribuidor_Update(request, slug):
    contribuidores = m.Contribuidor.objects.all()
    update_contribuidor = m.Contribuidor.objects.get(slug=slug)

    if request.method == 'POST':
        contribuidorEdit = f.ContribuidorForm(request.POST, request.FILES, instance=update_contribuidor)
        if contribuidorEdit.is_valid():
            contribuidorEdit = contribuidorEdit.save(commit=False)
            contribuidorEdit.save()

            messages.info(request, f'Contribuidor {contribuidorEdit.contribuidor} foi Editado!')
            return redirect('Contribuidor_read', slug=update_contribuidor.slug)
    else:
        contribuidorEdit = f.ContribuidorForm(instance=update_contribuidor)

    return render(request, 'create_Contribuidor.html', {'formCon': contribuidorEdit, 'contribuidores':contribuidores})




# # # DELETING

@login_required
def produto_Delete(request, slug):
    delete_produto = m.Produto.objects.get(slug=slug)
    delete_produto.delete()

    messages.info(request, f'Produto {delete_produto.produto} foi Excluido!')
    return redirect('produtos')


@login_required
def categoria_Delete(request, slug):
    delete_categoria = m.Categoria.objects.get(slug=slug)
    delete_categoria.delete()

    messages.info(request, f'Categoria {delete_categoria.categoria} foi Excluido!')
    return redirect('CategoriaForm')


@login_required
def contribuidor_Delete(request, slug):
    delete_contribuidor = m.Contribuidor.objects.get(slug=slug)
    delete_contribuidor.delete()

    messages.info(request, f'Contribuidor {delete_contribuidor.contribuidor} foi Excluido!')
    return redirect('contribuidores')
