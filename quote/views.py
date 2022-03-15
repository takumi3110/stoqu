from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


@login_required()
def genre_select(request):
    return render(request, 'quote/genre.html')


@login_required()
def quote_order(request, **kwargs):
    context = {
        'genre': kwargs['genre']
    }
    return render(request, 'quote/order.html', context)
