from django.shortcuts import render, redirect
from . import models as m, forms as f

def home(request):
    return render(request, 'home.html')

def estoque(request):
    estoque = m.Produto.objects.all()
    return render (request, 'listEstoque.html', {'list':estoque})

def fornecedor(request):
    contribuidor = m.Contribuidor.objects.all()
    return render (request, 'listContribuidores.html', {'list':contribuidor})




# # # CREATING # # #
def produto_Create(request):
    produtoForm = f.ProdutoForm(request.POST or None, request.FILES or None)

    if produtoForm.is_valid():
        produtoForm.save()
        return redirect('estoque')
    else:
        return render(request, 'P-form.html', {'Pform':produtoForm})

        
def category_Create(request):
    categoryForm = f.CategoryForm(request.POST or None, request.FILES or None)

    if categoryForm.is_valid():
        categoryForm.save()
        return redirect('estoque')
    else:
        return render(request, 'C-form.html', {'Cform':categoryForm})


def fornercedor_Create(request):
    contribForm = f.ContribuidorForm(request.POST or None, request.FILES or None)

    if contribForm.is_valid():
        contribForm.save()
        return redirect('estoque')
    else:
        return render(request, 'F-form.html', {'Fform':contribForm})