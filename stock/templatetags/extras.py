# -*- coding:utf-8 -*-

from django import template

register = template.Library()


@register.filter
def none_check(value):
	if value is None:
		return '-'
	else:
		return value
