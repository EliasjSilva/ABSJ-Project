from django import forms as forms
from . import models as m # Vai importar os modelos do models como 'm'
from django.utils.html import format_html
from datetime import date

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
            'validade': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',

                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuração da data mínima com base na instância
        if self.instance and self.instance.validade:
            self.fields['validade'].widget.attrs['min'] = str(self.instance.validade)
    
    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        contribuidor = cleaned_data.get('contribuidor')
        codigo = cleaned_data.get('codigo')

        # Muda o campo escrito para capitalize na hora de Salvar para não gerar conflitos como 'oi', 'OI' e 'Oi'
        produto = produto.capitalize()

        # Verifica a instancia do objeto na hora do cadastro ou edição para uma validação
        for instance in m.Produto.objects.all():
            # Se o objeto instanciado estiver sendo editado e não houver alteração, retorna o valor normal
            if self.instance and self.instance.produto == produto and self.instance.contribuidor == contribuidor:
                return cleaned_data

        # Verifica se já existe um produto com o mesmo nome para o mesmo contribuidor
        if produto and contribuidor:
            exists = m.Produto.objects.filter(produto=produto, contribuidor=contribuidor).exists()
            if exists:
                error_message = format_html('Este produto já está cadastrado para o contribuidor <span class="error-var">{}</span>.', contribuidor)
                self.add_error('produto', error_message)

        return cleaned_data



    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']

        if len(str(codigo)) > 13 or len(str(codigo)) < 13:
            error_message = format_html('Código de Barras requerido um total de 13 digitos.')
            raise forms.ValidationError(error_message)

        for instance in m.Produto.objects.all():
            if self.instance and self.instance.codigo == codigo:
                return codigo

            if instance.codigo == codigo:
                error_message = format_html('Já possui um Código de Barras no sistema com essa numeração <span class="error-var">{}</span>.', instance.codigo)
                raise forms.ValidationError(error_message)

        return codigo

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()

        # Configuração da data mínima com base na instância
        if self.instance and self.instance.validade:
            self.fields['validade'].widget.attrs['min'] = str(self.instance.validade)
        else:
            self.fields['validade'].widget.attrs['min'] = str(date.today())




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
            'tempo': forms.TextInput(
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

        self.fields['tempo'].widget.attrs['max'] = date.today()

        # Personalize a renderização do campo tempo ao editar
        # instance = kwargs.get('instance')
        # if instance and instance.tempo:
        #     self.fields['tempo'].widget.attrs['value'] = instance.tempo.strftime('%d-%m-%Y')



class MovimentoForm(forms.ModelForm):
    class Meta:
        model = m.Movimento
        fields = ['user', 'produto', 'quantidade', 'tipo']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
            cleaned_data = super().clean()
            tipo = cleaned_data.get('tipo')
            quantidade = cleaned_data.get('quantidade')
            produto = cleaned_data.get('produto')

            if tipo == 'Saída':
                if produto and produto.estoque <= 0:
                    error_message = format_html('O estoque para o produto <span class="error-var">{}</span> está zerado.', produto)
                    self.add_error('tipo', error_message)

            return cleaned_data



    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MovimentoForm, self).__init__(*args, **kwargs)
        # self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['produto'].widget = forms.HiddenInput()

