from django.urls import path
from .views import (
    DashboardView,
    NovoPedido,
    NovoItemPedido,
    ListaVendas,
    EditPedido,
    DeletePedido,
)

urlpatterns = [
    path('', ListaVendas.as_view(), name="lista-vendas"),
    path('novo-pedido/', NovoPedido.as_view(), name="novo_pedido"),
    path('edit-pedido/<int:venda>/', EditPedido.as_view(), name="edit_item_pedido"),
    path('delete-pedido/<int:venda>/', DeletePedido.as_view(), name="delete_item_pedido"),
    path('novo-item-pedido/<int:venda>/', NovoItemPedido.as_view(), name="novo_item_pedido"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]

