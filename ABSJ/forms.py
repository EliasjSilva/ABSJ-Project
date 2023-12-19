from django import forms
from . import models as m # Vai importar os modelos do models como 'm'

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = m.Produto
        fields = ['categoria', 'contribuidor', 'produto', 'qtd', 'validade', 'user']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'contribuidor': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'qtd': forms.NumberInput(attrs={'class': 'form-control'}),
            'validade': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }

    def clean_produto(self):
            produto = self.cleaned_data['produto']
            return produto.capitalize()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = m.Categoria
        fields = "__all__"
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
                
    def clean_category(self):
            category = self.cleaned_data['category']
            return category.capitalize()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

class ContribuidorForm(forms.ModelForm):
    class Meta:
        model = m.Contribuidor
        fields = "__all__"
        widgets = {
            'contribuidor': forms.TextInput(attrs={'class': 'form-control'}),
            'tipocontribuidor': forms.Select(attrs={'class': 'form-control'}),
            'tempo': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    
                }
            ),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
                
    def clean_contribuidor(self):
            contribuidor = self.cleaned_data['contribuidor']
            return contribuidor.capitalize()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContribuidorForm, self).__init__(*args, **kwargs)
