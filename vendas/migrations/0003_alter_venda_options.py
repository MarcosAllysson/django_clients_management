# Generated by Django 3.2.6 on 2021-08-14 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0002_auto_20210812_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venda',
            options={'permissions': [('setar_nfe', 'Usuário pode alterar parametro NFE')]},
        ),
    ]