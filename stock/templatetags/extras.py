# -*- coding:utf-8 -*-

from django import template

register = template.Library()


@register.filter
def boolean_check(value):
	if value:
		return value
	elif value is None:
		return '不明'
	else:
		return 'なし'
