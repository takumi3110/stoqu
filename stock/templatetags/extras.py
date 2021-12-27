# -*- coding:utf-8 -*-

from django import template

register = template.Library()


@register.filter
def boolean_check(value):
	if value:
		return value
	else:
		return 'なし'
