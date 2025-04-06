# Generated by Django 5.0 on 2025-04-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABSJ', '0026_categoria_slug_contribuidor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribuidor',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
