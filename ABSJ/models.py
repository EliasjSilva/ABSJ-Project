from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils.html import format_html

CONTRIBUIDOR = [
    ('Doador', 'Doador'),
    ('Fornecedor', 'Fornecedor'),
]
MOVIMENTO = [
    ('Entrada', 'Entrada'),
    ('Saída', 'Saída'),
]

class Categoria(models.Model):
    categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['categoria']

    def __str__(self):
        return self.categoria







class Contribuidor(models.Model):
    contribuidor = models.CharField(max_length=250, unique=True)
    tipocontribuidor = models.CharField(choices=CONTRIBUIDOR, max_length=10)
    tempo = models.DateField()
    tempo_ultima_atualizacao = models.DateField(default=date.today)
    quantidade_dias = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['tempo']

    def __str__(self):
        return self.contribuidor
        
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
        return self.produto

    def calcular_tempo_validade(self):
        hoje = date.today()
        diferenca = relativedelta(self.validade, hoje)

        # Valor não negativo 'abs'
        meses = diferenca.months
        dias = diferenca.days
        return meses, dias


    def salvar_alteracoes(self):
        hoje = date.today()
        diferenca = relativedelta( self.validade, hoje)
        self.quantidade_dias = diferenca.days
        self.save()


    def proximo_vencimento(self, dias_limite=7):
        """
        Verifica se o produto está próximo do vencimento.
        Retorna True se estiver próximo, False caso contrário.
        """
        hoje = date.today()
        diferenca = (self.validade - hoje).days
        return 0 < diferenca <= dias_limite

    def notificacao(self):
        """
        Obtém uma mensagem de notificação para o produto.
        A mensagem depende da proximidade do vencimento.
        """
        if self.proximo_vencimento():
            return format_html('<span class="error-var">{}</span> expira no dia {}!', self.produto, self.validade )
        else:
            return ""





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