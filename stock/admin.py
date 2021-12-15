from django.contrib import admin

from .models import Option, Base, Storage


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('maker', 'name', 'price', 'quantity')
	list_display_links = ('maker', 'name', 'price', 'quantity')
	list_filter = ('maker', 'name')
	search_fields = ('maker', 'name')
	actions_on_bottom = True


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
	list_display = ('base', 'order_number', 'item', 'price', 'quantity')
	list_display_links = ('base', 'order_number', 'item', 'price', 'quantity')
	list_filter = ('order_number', 'item', 'base')
	search_fields = ('order_number', 'item', 'base')
	actions_on_bottom = True


admin.site.register(Base)
