# Generated by Django 5.0 on 2023-12-24 23:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABSJ', '0018_remove_contribuidor_tempo_ultima_atualizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribuidor',
            name='tempo_ultima_atualizacao',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
