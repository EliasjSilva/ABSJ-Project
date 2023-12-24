from django import forms as forms
from . import models as m # Vai importar os modelos do models como 'm'
from django.utils.html import format_html

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = m.Produto
        fields = ['categoria', 'contribuidor', 'produto', 'validade', 'user', 'estoque', 'codigo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'contribuidor': forms.Select(attrs={'class': 'form-select'}),
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'validade': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }

    def clean_produto(self):
        produto = self.cleaned_data['produto']

        # Muda o campo escrito para capitalize na hora de Salvar para não gerar complitos como 'oi', 'OI' e 'Oi'
        produto = produto.capitalize()

        # Verifica a instancia do objeto na hora do cadastro ou edição para uma validação
        for instance in m.Produto.objects.all():
            # Se o obejto instanciado estiver sendo editado e não houver alteração retonna o valor normal
            if self.instance and self.instance.produto == produto:
                return produto

            # Se for criado um novo produto e a instancia já estiver no sistema retona o erro.
            if instance.produto == produto:
                error_message = format_html('Já possui uma Produto no sistema com o nome <span class="error-var">{}</span>.', instance.produto)
                raise forms.ValidationError(error_message)

        return produto


    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']

        if len(str(codigo)) > 13 or len(str(codigo)) < 13:
            error_message = format_html('Código de Barras requerido um total de 13 digitos.')
            raise forms.ValidationError(error_message)

        # Verifica a instancia do objeto na hora do cadastro ou edição para uma validação
        for instance in m.Produto.objects.all():
            # Se o obejto instanciado estiver sendo editado e não houver alteração retonna o valor normal
            if self.instance and self.instance.codigo == codigo:
                return codigo

            # Se for criado um novo codigo e a instancia já estiver no sistema retona o erro.
            if instance.codigo == codigo:
                error_message = format_html('Já possui uma Código no sistema com essa numeração <span class="error-var">{}</span>.', instance.codigo)
                raise forms.ValidationError(error_message)

        return codigo

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = m.Categoria
        fields = "__all__"
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }
                
    def clean_categoria(self):
            categoria = self.cleaned_data['categoria']
            categoria = categoria.capitalize()

            for instance in m.Categoria.objects.all():

                if self.instance and self.instance.categoria == categoria:
                    return categoria

                if instance.categoria == categoria:
                    error_message = format_html('Já possui uma Categoria no sistema com o nome <span class="error-var">{}</span>.', instance.categoria)
                    raise forms.ValidationError(error_message)
            return categoria

            

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoriaForm, self).__init__(*args, **kwargs)



class ContribuidorForm(forms.ModelForm):
    class Meta:
        model = m.Contribuidor
        fields = ['contribuidor', 'tipocontribuidor', 'tempo', 'observacoes']
        widgets = {
            'contribuidor': forms.TextInput(attrs={'class': 'form-control'}),
            'tipocontribuidor': forms.Select(attrs={'class': 'form-select'}),
            'tempo': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    
                }
            ),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
                
    def clean_contribuidor(self):
            contribuidor = self.cleaned_data['contribuidor']
            contribuidor = contribuidor.capitalize()

            for instance in m.Contribuidor.objects.all():

                if self.instance and self.instance.contribuidor == contribuidor:
                    return contribuidor

                if instance.contribuidor == contribuidor:
                    error_message = format_html('Já possui um Contribuidor no sistema com o nome <span class="error-var">{}</span>.', instance.contribuidor)
                    raise forms.ValidationError(error_message)
            return contribuidor


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContribuidorForm, self).__init__(*args, **kwargs)



class MovimentoForm(forms.ModelForm):
    class Meta:
        model = m.Movimento
        fields = ['user', 'produto', 'quantidade', 'tipo']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
        }
            

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MovimentoForm, self).__init__(*args, **kwargs)
        # self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['produto'].widget = forms.HiddenInput()

