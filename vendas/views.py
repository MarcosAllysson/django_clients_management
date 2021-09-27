from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from vendas.models import Venda
from .forms import ItemPedidoForm
from .models import ItemDoPedido

# LOGGING
# import logging
# logger = logging.getLogger('django')


# Create your views here.
class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Você não tem permissão para visualizar esta página.')
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    """
    Informações gerais sobre as vendas
    """

    def get(self, request):
        result = dict()

        # Calculando média do valor do model Venda
        # media = Venda.objects.all().aggregate(Avg('valor'))['valor__avg']
        media = Venda.objects.media()

        # Calculando média de desconto do model Venda
        # media_desconto = Venda.objects.all().aggregate(Avg('desconto'))['desconto__avg']
        media_desconto = Venda.objects.media_desconto()

        # Menor pedido
        # menor_pedido = Venda.objects.all().aggregate(Min('valor'))['valor__min']
        menor_pedido = Venda.objects.menor_pedido()

        # Maior pedido
        maior_pedido = Venda.objects.maior_pedido()

        # Número de pedidos
        # numero_pedidos = Venda.objects.all().aggregate(Count('id'))['id__count']
        numero_pedidos = Venda.objects.numero_pedidos()

        # numero_pedidos_nfe = Venda.objects.filter(nfe_emitida=True).aggregate(Count('id'))['id__count']
        numero_pedidos_nfe = Venda.objects.numero_pedidos_nfe()

        # Outra opção:
        # numero_pedidos = Venda.objects.all().count()

        # Soma dos valores
        soma_valores_pedidos = Venda.objects.all().aggregate(Sum('valor'))['valor__sum']

        result['media'] = f'{media:.2f}'
        result['media_desconto'] = f'{media_desconto:.2}'
        result['menor_pedido'] = f'{menor_pedido:.2f}'
        result['maior_pedido'] = f'{maior_pedido:.2f}'
        result['numero_pedidos'] = numero_pedidos
        result['numero_pedidos_nfe'] = numero_pedidos_nfe
        result['soma_valores_pedidos'] = f'{soma_valores_pedidos:.2f}'
        return render(request, 'vendas/dashboard.html', result)


class NovoPedido(View):
    def get(self, request):
        result = {}
        return render(request, 'vendas/novo_pedido.html', result)

    def post(self, request):
        data = {'form': ItemPedidoForm(),
                'numero': request.POST['numero'],
                'desconto': float(request.POST['desconto'].replace(',', '.')),
                'venda_id': request.POST['venda_id']
                }

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
            venda.desconto = data['desconto']
            venda.numero = data['numero']
            venda.save()

        else:
            venda = Venda.objects.create(
                numero=data['numero'], desconto=data['desconto']
            )

        items = venda.itemdopedido_set.all()
        data['venda'] = venda
        data['items'] = items

        return render(request, 'vendas/novo_pedido.html', data)


class NovoItemPedido(View):
    def get(self, request, venda):
        pass

    def post(self, request, venda):
        data = {}

        item = ItemDoPedido.objects.filter(produto_id=request.POST['produto_id'], venda_id=venda).exists()

        if item:
            data['mensagem'] = 'Item já incluído no pedido. Edite-o!'
            item = item[0]

        else:
            item = ItemDoPedido.objects.create(
                produto_id=request.POST['produto_id'], quantidade=request.POST['quantidade'],
                desconto=request.POST['desconto'], venda_id=venda)

        data['items'] = item
        data['form'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(request, 'vendas/novo_pedido.html', data)


class ListaVendas(View):
    # logger.debug('Acessaram listagem de vendas')

    def get(self, request):
        vendas = Venda.objects.all()
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas})


class EditPedido(View):
    def get(self, request, venda):
        data = {}

        try:
            venda = Venda.objects.get(id=venda)
            data['form'] = ItemPedidoForm()
            data['numero'] = venda.numero
            data['desconto'] = float(venda.desconto)
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()

            return render(request, 'vendas/novo_pedido.html', data)

        except Venda.DoesNotExist:
            return HttpResponse('<h1>Objeto não existe</h1>')


class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)

        return render(request, 'vendas/delete_pedido_confirm.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()

        return redirect('lista-vendas')
