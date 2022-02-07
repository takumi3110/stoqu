from django import template

from stock.models import StorageCart, StorageItem, OrderItem

register = template.Library()


def make_subtotal(cart):
	"""
	合計金額を出す
	:param cart:
	:return all_price:
	"""
	subtotal_price = 0
	for order_item in cart.order_item.all():
		item_price = order_item.storage_item.price
		quantity = order_item.quantity
		for option in order_item.storage_item.option.all():
			item_price += option.price
		subtotal_price += item_price * quantity
	return subtotal_price


def add_tax(price):
	"""
	:param
	:param price:
	:return round(sub_total):
	"""
	tax = 1.10
	sub_total = price * tax
	return round(sub_total)


@register.filter
def storage_count(user):
	if user.is_authenticated:
		cart_filter = StorageCart.objects.filter(requester=user, ordered=False)
		if cart_filter.exists():
			count = 0
			for cart in cart_filter:
				for order_item in cart.order_item.all():
					count += order_item.quantity
			return count
		return 0


@register.filter
def total_price(pk):
	order_item = OrderItem.objects.get(pk=pk)
	storage_item = order_item.storage_item
	all_option = storage_item.option.all()
	price = storage_item.price
	if all_option.exists():
		for option in all_option:
			price += option.price
	return price


@register.filter
def storage_subtotal(user):
	if user.is_authenticated:
		cart_filter = StorageCart.objects.filter(requester=user, ordered=False)
		if cart_filter.exists():
			price = 0
			for cart in cart_filter:
				price = make_subtotal(cart)
			return add_tax(price)
		return 0


@register.filter
def storage_kitting_price(user):
	if user.is_authenticated:
		cart_filter = StorageCart.objects.filter(requester=user, ordered=False)
		if cart_filter.exists():
			price = 0
			for cart in cart_filter:
				for order_item in cart.order_item.all():
					kitting_price = order_item.kitting_plan.price
					price += kitting_price * order_item.quantity
			return add_tax(price)


@register.filter
def storage_total_price(user):
	if user.is_authenticated:
		sub_total = storage_subtotal(user)
		kitting_price = storage_kitting_price(user)
		total = sub_total + kitting_price
		return total
