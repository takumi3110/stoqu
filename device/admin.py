from django.contrib import admin

from .models import CPU, Storage, PCSpec, PC, Item


class PCSpecInline(admin.TabularInline):
	model = PCSpec
	extra = 0
	fields = ('memory', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
	list_display = ('maker', 'name', 'gen')
	list_display_links = ('maker', 'name', 'gen')
	list_filter = ('maker', 'name', 'gen')
	search_fields = ('maker', 'name', 'gen')
	inlines = [PCSpecInline]


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
	list_display = ('type', 'size')
	list_display_links = ('type', 'size')
	list_filter = ('type', 'size')
	search_fields = ('type', 'size')
	inlines = [PCSpecInline]


@admin.register(PCSpec)
class PCSpecAdmin(admin.ModelAdmin):
	list_display = ('cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad')
	list_display_links = ('cpu', 'memory', 'storage', 'size')
	list_filter = ('cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan')
	search_fields = ('cpu', 'memory', 'storage', 'size')
	actions_on_bottom = True


@admin.register(PC)
class PCAdmin(admin.ModelAdmin):
	list_display = ('category', 'maker', 'name', 'model_number')
	list_display_links = ('category', 'maker', 'name', 'model_number')
	list_filter = ('category', 'maker', 'name', 'model_number')
	search_fields = ('category', 'maker', 'name', 'model_number')
	actions_on_bottom = True


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('pc', 'spec')
	list_display_links = ('pc', 'spec')
	search_fields = ('pc', 'spec')
	actions_on_bottom = True
