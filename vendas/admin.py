from django.contrib import admin
from .models import Venda, ItemDoPedido

# DJANGO ADMIN ACTION:
from vendas.actions import nfe_emitida
from vendas.actions import nfe_nao_emitida


# Register your models here.
class ItemPedidoInline(admin.TabularInline):
# class ItemPedidoInline(admin.StackedInline):
    model = ItemDoPedido
    extra = 1


class VendaAdmin(admin.ModelAdmin):
    readonly_fields = ('valor', )
    list_display = ('numero', 'valor', 'nfe_emitida')
    actions = [nfe_emitida, nfe_nao_emitida]
    inlines = [ItemPedidoInline]
    # filter_vertical = ['produtos', ]
    # filter_horizontal = ['produtos', ]
    # autocomplete_fields = ['pessoa', ]

    # def total(self, obj):
    #     return obj.get_total()
    # total.short_description = 'Total'


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)

