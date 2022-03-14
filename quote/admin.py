from django.contrib import admin

from .models import Item, Destination, QuoteItem, QuoteRequester, OrderItem, Cart, OrderInfo


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('genre', 'maker', 'name')
    list_display_links = ('genre', 'maker', 'name')
    list_filter = ('genre', 'maker')
    search_fields = ('genre', 'maker', 'name')
    actions_on_bottom = True


@admin.register(QuoteRequester)
class QuoteRequesterAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'team', 'addressee')
    list_display_links = ('last_name', 'first_name', 'team', 'addressee')
    list_filter = ('last_name', 'first_name', 'team', 'addressee')
    search_fields = ('last_name', 'first_name', 'team', 'addressee')
    actions_on_bottom = True 


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('number', 'item', 'quantity', 'ordered_at', 'arrived_at', 'delivery_at')
    list_display_links = ('number', 'item', 'quantity', 'ordered_at', 'arrived_at', 'delivery_at')
    list_filter = ('number', 'item', 'quantity', 'ordered', 'delivered')
    search_fields = ('number', 'item__name', 'quantity')
    actions_on_bottom = True


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('destination', 'quote_item')
    list_display_links = ('destination', 'quote_item')
    list_filter = ('destination',)
    search_fields = ('destination__name', 'quote_item_item__name')
    actions_on_bottom = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('requester', 'worker', 'ordered')
    list_display_links = ('requester', 'worker', 'ordered')
    list_filter = ('requester', 'worker', 'ordered')
    search_fields = ('requester', 'worker')
    filter_horizontal = ['order_item']
    actions_on_bottom = True 


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('status', 'number', 'ticket', 'worker', 'requester', 'registration_at', 'updated_at', 'finished')
    list_display_links = ('status', 'number', 'ticket', 'worker', 'requester', 'registration_at', 'updated_at', 'finished')
    list_filter = ('status', 'worker', 'requester', 'finished')
    search_fields = ('status', 'number', 'ticket', 'worker__screenname', 'requester__first_name')
    actions_on_bottom = True


admin.site.register(Destination)
