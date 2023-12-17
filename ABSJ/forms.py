from django import forms
from . import models as m

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = m.Produto
        fields = "__all__"
        widgets = {
            'validade': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = m.Categoria
        fields = "__all__"

class ContribuidorForm(forms.ModelForm):
    class Meta:
        model = m.Contribuidor
        fields = "__all__"
        widgets = {
            'tempo': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
        }