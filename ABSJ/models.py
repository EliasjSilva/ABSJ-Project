from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import text

CONTRIBUIDOR = [
    ('Doador', 'Doador'),
    ('Fornecedor', 'Fornecedor'),
]
MOVIMENTO = [
    ('Entrada', 'Entrada'),
    ('Saída', 'Saída'),
]

class Categoria(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['categoria']

    def save(self, *args, **kwargs):
        # Muda o campo escrito para capitalize na hora de Salvar para não gerar conflitos como 'oi', 'OI' e 'Oi'
        self.categoria = self.categoria.capitalize()

        # Gera o slug a partir do nome do categoria
        slug = text.slugify(self.categoria)    

        # Verifica se o slug está vazio e, se estiver, utiliza um valor padrão
        if not slug:
            slug = 'Categoria'
        counter = 1
        original_slug = slug
        while Categoria.objects.filter(slug=slug).exclude(id=self.id).exists() or None:
            slug = f"{original_slug}_{counter}"
            counter += 1

        self.slug = slug

        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.categoria.capitalize()


class Contribuidor(models.Model):
    slug = models.SlugField(unique=True)
    contribuidor = models.CharField(max_length=250, unique=True)
    tipocontribuidor = models.CharField(choices=CONTRIBUIDOR, max_length=10)
    tempo = models.DateField()
    tempo_ultima_atualizacao = models.DateField(default=date.today)
    quantidade_dias = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['tempo']

    def __str__(self):
        return self.contribuidor.capitalize()

    def save(self, *args, **kwargs):
        # Muda o campo escrito para capitalize na hora de Salvar para não gerar conflitos como 'oi', 'OI' e 'Oi'
        self.contribuidor = self.contribuidor.capitalize()

        # Gera o slug a partir do nome do contribuidor
        slug = text.slugify(self.contribuidor)    

        # Verifica se o slug está vazio e, se estiver, utiliza um valor padrão
        if not slug:
            slug = 'Contribuidor'
        counter = 1
        original_slug = slug
        while Contribuidor.objects.filter(slug=slug).exclude(id=self.id).exists() or None:
            slug = f"{original_slug}_{counter}"
            counter += 1

        self.slug = slug

        super(Contribuidor, self).save(*args, **kwargs)

    def contar_produtos(self):
        return Produto.objects.filter(contribuidor=self).count()
    
    def calcular_tempo_contribuicao(self):
        hoje = date.today()
        diferenca = relativedelta(hoje, self.tempo)
        anos = diferenca.years
        meses = diferenca.months
        dias = diferenca.days
        return anos, meses, dias

    def salvar_alteracoes(self):
        hoje = date.today()
        diferenca = relativedelta(hoje, self.tempo)
        self.quantidade_dias = diferenca.days
        self.save()




class Produto(models.Model):
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    contribuidor = models.ForeignKey(Contribuidor, on_delete=models.CASCADE, null=True)
    produto = models.CharField(max_length=200)
    codigo = models.PositiveIntegerField(unique=True)
    estoque = models.PositiveIntegerField(default=0)
    validade = models.DateField()

    tempo_ultima_atualizacao = models.DateField(default=date.today)
    quantidade_dias = models.IntegerField(default=0)

    class Meta:
        ordering = ['produto']

    def __str__(self):
        return self.produto.capitalize()

    def save(self, *args, **kwargs):
        # Muda o campo escrito para capitalize na hora de Salvar para não gerar conflitos como 'oi', 'OI' e 'Oi'
        self.produto = self.produto.capitalize()

        # Gera o slug a partir do nome do produto
        slug = text.slugify(self.produto)

        # Adiciona o contribuidor ao slug para garantir que seja único - não necessário, pois não vai ser ter 2 p para o mesmo c
        # slug = f"{slug}{self.contribuidor.id}"

        # Verifica se o slug está vazio e, se estiver, utiliza um valor padrão
        if not slug:
            slug = 'Produto'

        # Garante que o slug seja único
        counter = 1
        original_slug = slug

        # Enquanto o slug for identcio a um existente, ele vai ser excluido e pegará o original e adc sempre +1
        while Produto.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{original_slug}_{counter}"
            counter += 1

        self.slug = slug

        super(Produto, self).save(*args, **kwargs)
        

    def calcular_tempo_validade(self):
        hoje = date.today()
        diferenca = relativedelta(self.validade, hoje)

        # Valor não negativo 'abs' - removido para fazer os if passar da validade
        anos = diferenca.years
        meses = diferenca.months
        dias = diferenca.days
        return anos, meses, dias

    def salvar_alteracoes(self):
        hoje = date.today()
        diferenca = relativedelta( self.validade, hoje)
        self.quantidade_dias = diferenca.days
        self.save()





class Movimento(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=7, choices=MOVIMENTO)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modificado']


    def save(self, *args, **kwargs):

        # Atualiza o estoque do produto com base no tipo de movimento
        if self.tipo == 'Entrada':
            self.produto.estoque += self.quantidade
        elif self.tipo == 'Saída':
            self.produto.estoque -= self.quantidade
            if self.produto.estoque < 0:
                self.produto.estoque = 0

        super(Movimento, self).save(*args, **kwargs)
        self.produto.save()



# # # AREA DE TESTE # # #