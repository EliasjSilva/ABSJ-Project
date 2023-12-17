from django.db import models

CONTRIBUIDOR = [
    ('Doador', 'Doador'),
    ('Fornecedor', 'Fornecedor'),
]

class Categoria(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Contribuidor(models.Model):
    contribuidor = models.CharField(max_length=250)
    tipocontribuidor = models.CharField(choices=CONTRIBUIDOR, max_length=10)
    tempo = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.contribuidor


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    contribuidor = models.ForeignKey(Contribuidor, on_delete=models.CASCADE, null=True)
    produto = models.CharField(max_length=200)
    qtd = models.PositiveIntegerField(default=0)
    validade = models.DateField()
    entrada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.produto
