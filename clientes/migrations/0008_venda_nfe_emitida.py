# Generated by Django 3.2.6 on 2021-08-11 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_alter_venda_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='nfe_emitida',
            field=models.BooleanField(default=False),
        ),
    ]
