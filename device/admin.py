from django.contrib import admin

from .models import CPU, Storage, PC, PCDetail


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
	list_display = ('maker', 'name', 'gen')
	list_display_links = ('maker', 'name', 'gen')
	list_filter = ('maker', 'name', 'gen')
	search_fields = ('maker', 'name', 'gen')
	ordering = ['maker']


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
	list_display = ('type', 'size')
	list_display_links = ('type', 'size')
	list_filter = ('type', 'size')
	search_fields = ('type', 'size')
	ordering = ['size']


@admin.register(PC)
class PCAdmin(admin.ModelAdmin):
	list_display = ('category', 'maker', 'name', 'model_number')
	list_display_links = ('category', 'maker', 'name', 'model_number')
	list_filter = ('category', 'maker', 'name', 'model_number')
	search_fields = ('category', 'maker', 'name', 'model_number')
	actions_on_bottom = True
	ordering = ['category']


@admin.register(PCDetail)
class PCDetailAdmin(admin.ModelAdmin):
	list_display = ('pc', 'cpu', 'memory', 'storage', 'numpad')
	list_display_links = ('pc', 'cpu', 'memory', 'storage', 'numpad')
	list_filter = ('pc', 'cpu', 'memory', 'size', 'numpad')
	search_fields = ('pc', )
	actions_on_bottom = True
