from django import template

from stock.models import StorageCart, StorageItem, OrderItem

register = template.Library()


def make_subtotal(cart):
	"""
	合計金額を出す
	:param cart:
	:return all_price:
	"""
	price = 0
	for order_item in cart.order_item.all():
		item_price = order_item.storage_item.price
		quantity = order_item.quantity
		for option in order_item.storage_item.option.all():
			item_price += option.price
		price += item_price * quantity
	return price


@register.filter
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
def storage_count(pk):
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
def kitting_price(pk):
	cart = StorageCart.objects.get(pk=pk)
	result = 0
	for order_item in cart.order_item.all():
		price = order_item.kitting_plan.price
		result += price * order_item.quantity
	return add_tax(result)


@register.filter
def subtotal_price(pk):
	cart = StorageCart.objects.get(pk=pk)
	result = make_subtotal(cart)
	return add_tax(result)


@register.filter
def result_price(pk):
	cart = StorageCart.objects.get(pk=pk)
	subtotal = make_subtotal(cart)
	kitting = kitting_price(pk)
	result = add_tax(subtotal) + kitting
	return result


@register.simple_tag
def url_replace(request, field, value):
	dict_ = request.GET.copy()
	dict_[field] = value
	return dict_.urlencode()
