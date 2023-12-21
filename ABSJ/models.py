from django.db import models
from django.contrib.auth import get_user_model

CONTRIBUIDOR = [
    ('Doador', 'Doador'),
    ('Fornecedor', 'Fornecedor'),
]

class Categoria(models.Model):
    category = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.category


class Contribuidor(models.Model):
    contribuidor = models.CharField(max_length=250, unique=True)
    tipocontribuidor = models.CharField(choices=CONTRIBUIDOR, max_length=10)
    tempo = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['tempo']

    def __str__(self):
        return self.contribuidor


class Produto(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    contribuidor = models.ForeignKey(Contribuidor, on_delete=models.CASCADE, null=True)
    produto = models.CharField(max_length=200, unique=True)
    qtd = models.PositiveIntegerField(default=0)
    validade = models.DateField()
    entrada = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['produto']

    def __str__(self):
        return self.produto
