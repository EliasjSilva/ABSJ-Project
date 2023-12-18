from django import forms
from . import models as m
from .models import Contribuidor
from .models import Categoria
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'contribuidor': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'qtd': forms.NumberInput(attrs={'class': 'form-control'}),
            'validade': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContribuidorForm(forms.ModelForm):
    class Meta:
        model = Contribuidor
        fields = "__all__"
        widgets = {
            'contribuidor': forms.TextInput(attrs={'class': 'form-control'}),
            'tipocontribuidor': forms.TextInput(attrs={'class': 'form-control'}),
            'tempo': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
