from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from clientes.models import Person
from produtos.models import Produto

# AGREGAÇÃO
from django.db.models import Sum, F, FloatField, Max

# PRÓPRIO MANAGER
from .managers import VendaManager


# Create your models here.
class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    nfe_emitida = models.BooleanField(default=False)

    # Django Manager
    objects = VendaManager()

    # PERMISSÕES
    class Meta:
        permissions = [
            # NOME DA PERMISSÃO / DESCRIÇÃO
            ('setar_nfe', 'Usuário pode alterar parametro NFE'),
            ('ver_dashboard', 'Usuário pode visualizar dashboard')
        ]

    # FUNÇÕES AGREGADAS
    def calcular_total(self):
        """
        Função que usa F Expressions do Django calculando preço total.
        Usando aggregate, total_pedido recebe a soma da quantidade x preço do preço, e o resultado
        é um float. A soma retorna um dicionário, e a variável total acessa a chave, no qual tem o valor
        """
        total = self.itemdopedido_set.all().aggregate(
            total_pedido=Sum((F('quantidade') * F('produto__preco')) - F('desconto'), output_field=FloatField())
        )['total_pedido'] or 0

        total = total - float(self.impostos) - float(self.desconto)
        self.valor = total
        # self.save()
        Venda.objects.filter(id=self.id).update(valor=total)

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    desconto = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f'{self.venda.numero} - {self.produto.descricao}'


# DJANGO SIGNALS
@receiver(post_save, sender=ItemDoPedido)
def update_itemdospedido_total(sender, instance, **kwargs):
    # instance -> representa o objeto em si
    instance.venda.calcular_total()

    # total = instance.get_total()
    # Venda.objects.filter(id=instance.id).update(total=total)


@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance, **kwargs):
    instance.calcular_total()

