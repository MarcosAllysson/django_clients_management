from django.db import models
from django.db.models import Sum, Max, Avg, Min, Count


class VendaManager(models.Manager):
    def media(self):
        return self.all().aggregate(Avg('valor'))['valor__avg']

    def media_desconto(self):
        return self.all().aggregate(Avg('desconto'))['desconto__avg']

    def menor_pedido(self):
        return self.all().aggregate(Min('valor'))['valor__min']

    def maior_pedido(self):
        return self.all().aggregate(Max('valor'))['valor__max']

    def numero_pedidos(self):
        return self.all().aggregate(Count('id'))['id__count']

    def numero_pedidos_nfe(self):
        return self.filter(nfe_emitida=True).aggregate(Count('id'))['id__count']
