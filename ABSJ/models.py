from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    quantidade_dias = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['tempo']

    def __str__(self):
        return self.contribuidor
        
# # # Testando :C
    def calcular_quantidade_dias(self):
        # Ajuste para calcular a diferença em dias
        atual = timezone.now().date()
        diferenca_dias = (atual - self.tempo).days

        # Atualizar o campo quantidade_dias
        self.quantidade_dias = diferenca_dias
        self.save()

        return diferenca_dias


class Produto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    contribuidor = models.ForeignKey(Contribuidor, on_delete=models.CASCADE, null=True)
    produto = models.CharField(max_length=200, unique=True)
    estoque = models.PositiveIntegerField(default=0)
    validade = models.DateField()

    class Meta:
        ordering = ['produto']

    def __str__(self):
        return self.produto

class Movimento(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=7, choices=MOVIMENTO)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modificado']