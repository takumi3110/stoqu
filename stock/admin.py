from django.contrib import admin

from .models import *


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('maker', 'name', 'price', 'quantity')
	list_display_links = ('maker', 'name', 'price', 'quantity')
	list_filter = ('maker', 'name')
	search_fields = ('maker', 'name')
	actions_on_bottom = True


@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
	list_display = ('base', 'order_number', 'item', 'price', 'quantity', 'registration_at')
	list_display_links = ('base', 'order_number', 'item', 'price', 'quantity', 'registration_at')
	list_filter = ('order_number', 'base')
	search_fields = ('order_number', 'item', 'base')
	actions_on_bottom = True
	filter_horizontal = ['option']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('storage_item', 'quantity', 'ordered', 'kitting_plan', 'requester')
	list_display_links = ('storage_item', 'quantity', 'kitting_plan', 'requester')
	list_filter = ('ordered', 'kitting_plan')
	search_fields = ('storage_item',)
	actions_on_bottom = True


@admin.register(StorageCart)
class StorageCartAdmin(admin.ModelAdmin):
	list_display = ('requester', 'ordered')
	list_display_links = ('requester',)
	list_filter = ('requester', 'ordered')
	search_fields = ('requester',)
	actions_on_bottom = True
	filter_horizontal = ['order_item']


@admin.register(Approve)
class ApproveAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'dept_code', 'dept_name')
	list_display_links = ('last_name', 'first_name', 'dept_code', 'dept_name')
	list_filter = ('last_name', 'first_name', 'dept_code', 'dept_name')
	search_fields = ('last_name', 'first_name', 'dept_code', 'dept_name')
	actions_on_bottom = True


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
	list_display = ('number', 'ticket', 'approve', 'requester', 'contact_user', 'ordered_at')
	list_display_links = ('number', 'ticket', 'approve', 'requester', 'contact_user', 'ordered_at')
	list_filter = ('approve', 'requester', 'contact_user')
	search_fields = ('number', 'ticket', 'approve', 'requester')
	actions_on_bottom = True


admin.site.register(KittingPlan)
