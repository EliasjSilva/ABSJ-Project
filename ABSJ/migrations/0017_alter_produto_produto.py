# Generated by Django 5.0 on 2023-12-24 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABSJ', '0016_alter_produto_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='produto',
            field=models.CharField(max_length=200),
        ),
    ]
