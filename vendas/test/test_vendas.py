from django.test import TestCase
from vendas.models import Venda, ItemDoPedido
from produtos.models import Produto


class VendaTestCase(TestCase):
    def setup(self):
        self.venda = Venda.objects.create(numero='123')
        self.produto = Produto.objects.create(descricao='Produto 1', preco=10)

    def test_verifica_numero_venda(self):
        # assert valida se a operação dado está ou não correta
        Venda.objects.create(numero='123')
        count = Venda.objects.all().count()
        self.assertEqual(Venda.objects.all().count(), count)

    # def test_valor_venda(self):
    #     ItemDoPedido.objects.create(venda=self.venda, produto=self.produto, quantidade=10, desconto=10)
    #
    #     self.assertEqual(self.venda.valor, 90)
        # assert self.venda.valor == 90
