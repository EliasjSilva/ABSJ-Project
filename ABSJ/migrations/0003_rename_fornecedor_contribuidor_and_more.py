# Generated by Django 5.0 on 2023-12-13 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ABSJ', '0002_remove_categoria_produto_remove_fornecedor_produto_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fornecedor',
            new_name='Contribuidor',
        ),
        migrations.RenameField(
            model_name='contribuidor',
            old_name='forneceddor',
            new_name='contribuidor',
        ),
        migrations.RenameField(
            model_name='contribuidor',
            old_name='tipoFornecedor',
            new_name='tipocontribuidor',
        ),
        migrations.RenameField(
            model_name='produto',
            old_name='fornecedor',
            new_name='contribuidor',
        ),
    ]