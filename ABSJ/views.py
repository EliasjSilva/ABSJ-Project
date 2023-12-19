from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m, forms as f

def home(request):
    return render(request, 'home.html')

def estoque(request):
    estoque = m.Produto.objects.all()
    return render (request, 'list_Estoque.html', {'estoque':estoque})

def fornecedor(request):
    contribuidor = m.Contribuidor.objects.all()
    return render (request, 'list_Contribuidores.html', {'contribuidor':contribuidor})




# # # CREATING # # #
def produto_Create(request):
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None, user=request.user)

    if produtoForm.is_valid():
        produtoForm.save()

        messages.info(request, 'Produto cadastrado com Sucesso!')
        return redirect('estoque')
    else:
        return render(request, 'create_Produto.html', {'Pform':produtoForm})

        
def category_Create(request):
    categoryForm = f.CategoryForm(request.POST or None, request.FILES or None, user=request.user)

    if categoryForm.is_valid():
        categoryForm.save()

        messages.info(request, 'Categoria adicionada com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Category.html', {'Cform':categoryForm})


def fornercedor_Create(request):
    contribForm = f.ContribuidorForm(request.POST or None, request.FILES or None, user=request.user)

    if contribForm.is_valid():
        contribForm.save()

        messages.info(request, 'Contribuidor adicionado com êxito!')
        return redirect('estoque')
    else:
        return render(request, 'create_Contribuidor.html', {'Fform':contribForm})


# # # READING
def produto_Read(request, id):
    read_produto = m.Produto.objects.get(id=id)
    return render(request, 'read_Produto.html', {'readP':read_produto})