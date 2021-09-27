# Generated by Django 3.2.6 on 2021-08-12 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_venda_nfe_emitida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='produtos',
        ),
        migrations.CreateModel(
            name='ItemDoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.FloatField()),
                ('desconto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.venda')),
            ],
        ),
    ]
