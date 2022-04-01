from django import template

from quote.models import QuoteItem

register = template.Library()


@register.simple_tag
def item_count(user):
    item = QuoteItem.objects.filter(worker=user, entered=False)
    if item:
        return len(item)
    else:
        return 0
