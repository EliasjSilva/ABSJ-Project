from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m, forms as f
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def estoque(request):
    produtos = m.Produto.objects.all()
    return render (request, 'list_Estoque.html', {'produtos':produtos})

@login_required
def fornecedor(request):
    contribuidor = m.Contribuidor.objects.all()
    return render (request, 'list_Contribuidores.html', {'contribuidor':contribuidor})




# # # CREATING # # #
@login_required
def produto_Create(request):
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None, user=request.user)

    if produtoForm.is_valid():
        produtoForm.save()

        messages.info(request, 'Produto cadastrado com Sucesso!')
        return redirect('estoque')
    else:
        return render(request, 'create_Produto.html', {'formPro':produtoForm})

@login_required
def category_Create(request):
    categoryForm = f.CategoryForm(request.POST or None, request.FILES or None, user=request.user)

    if categoryForm.is_valid():
        categoryForm.save()

        messages.info(request, 'Categoria adicionada com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Category.html', {'formCat':categoryForm})

@login_required
def fornercedor_Create(request):
    contribForm = f.ContribuidorForm(request.POST or None, request.FILES or None, user=request.user)

    if contribForm.is_valid():
        contribForm.save()

        messages.info(request, 'Contribuidor adicionado com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Contribuidor.html', {'formCon':contribForm})


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
    return render(request, 'read_Category.html', {'readCat':read_Cateogry})