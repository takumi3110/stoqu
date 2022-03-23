from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

from rest_framework import viewsets
from bootstrap_modal_forms.generic import BSModalCreateView

from .models import Item, QuoteItem, Destination, QuoteRequester, OrderItem, Cart, OrderInfo
from device.models import PC, PCDetail, Storage, CPU
from .serializers import QuoteItemSerializer
from .filters import QuoteItemFilter
from .forms import DestinationCreateBSModalForm

import datetime


class QuoteItemViewSet(viewsets.ModelViewSet):
    queryset = QuoteItem.objects.all()
    serializer_class = QuoteItemSerializer
    filter_class = QuoteItemFilter


def get_pc(category, maker, cpu, memory, storage):
    storage_size = Storage.objects.get_or_create(type=1, size=storage)[0]
    get_cpu = CPU.objects.get(name=cpu, latest=True)
    pc_list = PC.objects.filter(category=category, maker=maker)
    result = []
    for pc in pc_list:
        pc_detail_list = PCDetail.objects.filter(
            pc=pc,
            cpu=get_cpu,
            memory=memory,
            storage=storage_size,
        )
        for detail in pc_detail_list:
            result.append(detail)
    return result


def create_quote_item(genre, maker, name, quantity, worker, spec=None):
    item = Item.objects.get_or_create(
        genre=genre,
        maker=maker,
        name=name,
        spec=spec
    )
    item_filter = QuoteItem.objects.filter(item=item[0], worker=worker, ordered=False)
    quote_item_filter = QuoteItem.objects.filter(worker=worker, ordered=False)
    if quote_item_filter:
        last_item = quote_item_filter.last()
        if item_filter:
            for item in item_filter:
                item.quantity += int(quantity)
                item.save()
        else:
            QuoteItem.objects.create(
                number=last_item.number + 1,
                item=item[0],
                quantity=quantity,
                worker=worker
            )
    else:
        QuoteItem.objects.create(
            number=1,
            item=item[0],
            quantity=quantity,
            worker=worker
        )


@login_required()
def genre_select(request):
    return render(request, 'quote/genre.html')


@login_required()
def quote_order(request, **kwargs):
    genre = kwargs['genre']
    context = {
        'genre': genre
    }
    if request.method == 'POST':
        maker = request.POST['maker']
        spec = request.POST['spec']
        quantity = request.POST['quantity']
        worker = request.user
        if maker == 'none' or maker == '':
            maker = 'メーカー問わず'
        if genre == 'pc':
            category = request.POST['category']
            ten_key = request.POST['ten_key']
            cpu = request.POST['cpu']
            lanscope = request.POST['lanscope']
            office = request.POST['office']
            if cpu == 'i3':
                cpu = 'Core i3'
            elif cpu == 'i5':
                cpu = 'Core i5'
            elif cpu == 'i7':
                cpu = 'Core i7'
            memory = request.POST['memory']
            storage = request.POST['storage']
            search_stock = get_pc(category, maker, cpu, memory, storage)
            if search_stock:
                context['search_stock'] = search_stock
                return render(request, 'quote/order.html', context)
            if category == 'note':
                genre = 'ノートPC'
                name = 'ノートPC'
            elif category == 'desktop':
                genre = 'デスクトップPC'
                name = 'デスクトップPC'
            elif category == 'mini':
                genre = 'ミニPC'
                name = 'ミニPC'
            if category == 'note':
                spec_text = 'cpu:{}\nメモリ:{}GB\nストレージ:SSD{}GB\nテンキー:{}\n指紋認証:あり'\
                    .format(cpu, memory, storage, ten_key)
            else:
                spec_text = 'cpu:{}\nメモリ:{}GB\nストレージ:SSD{}GB\n'.format(cpu, memory, storage)
            if lanscope == 'true':
                license_name = 'Lanscope'
                license_maker = 'ソフトクリエイト'
                license_genre = 'License'
                create_quote_item(license_genre, license_maker, license_name, quantity, worker)
            elif office != 'none':
                license_name = 'Office'
                license_maker = 'Microsoft'
                license_genre = 'License'
                create_quote_item(license_genre, license_maker, license_name, quantity, worker)
        elif genre == 'display':
            genre = 'モニター'
            size = request.POST['size']
            detail = ''
            if 'hdmi' in request.POST.keys():
                hdmi = request.POST['hdmi'] + '\n'
                detail += hdmi
            if 'vga' in request.POST.keys():
                vga = request.POST['vga'] + '\n'
                detail += vga
            if 'dp' in request.POST.keys():
                dp = request.POST['dp'] + '\n'
                detail += dp
            name = '{}インチモニター'.format(size)
            spec_text = '{}\n{}インチ\nワイドモニター\n{}'.format(spec, size, detail)
        elif genre == 'others':
            genre = '周辺機器'
            name = request.POST['name']
            spec_text = spec
        elif genre == 'license':
            genre = 'License'
            name = request.POST['name']
            spec_text = spec
        create_quote_item(genre, maker, name, quantity, worker, spec=spec_text)
        new_quote_item = QuoteItem.objects.filter(worker=worker, ordered=False)
        for i, quote_item in enumerate(new_quote_item):
            quote_item.number = i + 1
            quote_item.save()
        context['quoteitem_list'] = new_quote_item
        return redirect('quote:item_list')
    else:
        return render(request, 'quote/order.html', context)


class QuoteItemList(LoginRequiredMixin, ListView):
    model = QuoteItem
    template_name = 'quote/item_list.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(QuoteItemList, self).get_queryset()
        qs = queryset.filter(worker=self.request.user, ordered=False)
        return qs
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(QuoteItemList, self).get_context_data(*args, **kwargs)
        quote_item = QuoteItem.objects.filter(worker=self.request.user, ordered=False)
        count = len(quote_item)
        context['count'] = count
        quantity = [i for i in range(100)]
        context['quantity'] = quantity
        return context


@login_required()
def delete_quote_item(request, pk):
    quote_item = QuoteItem.objects.get(pk=pk)
    quote_item.delete()
    quote_item_filter = QuoteItem.objects.filter(worker=request.user, ordered=False)
    for i, item in enumerate(quote_item_filter):
        item.number = i + 1
        item.save()
    return redirect('quote:item_list')


@login_required()
def register_destination(request):
    destination_list = Destination.objects.all()
    quoteitem_list = QuoteItem.objects.filter(worker=request.user, ordered=False)
    if request.method == 'POST':
        post_name_list = [destination.pk for destination in destination_list]
        cart = Cart.objects.get_or_create(worker=request.user, ordered=False)
        for post_name in post_name_list:
            if str(post_name) in request.POST:
                id_get_list = request.POST.getlist(str(post_name))
                for get_id in id_get_list:
                    quote_item = QuoteItem.objects.get(pk=get_id)
                    order_item = OrderItem.objects.get_or_create(
                        destination_id=post_name,
                        quote_item=quote_item,
                        delivered=False
                    )
                    cart[0].order_item.add(order_item[0])
        cart[0].save()
        return redirect('quote:add_requester')
    context = {
        'destination_list': destination_list,
        'quoteitem_list': quoteitem_list,
        'count': len(quoteitem_list)
    }
    return render(request, 'quote/destination.html', context)


class AddDestination(LoginRequiredMixin, BSModalCreateView):
    model = Destination
    template_name = 'snippets/create_modal.html'
    form_class = DestinationCreateBSModalForm
    success_url = reverse_lazy('quote:register_destination')


@login_required()
def add_requester(request):
    if request.method == 'POST':
        cart = Cart.objects.get(worker=request.user, ordered=False)
        last_name = request.POST['lastName']
        first_name = request.POST['firstName']
        team = request.POST['team']
        addressee = request.POST['addressee']
        ticket = request.POST['ticket']
        today = datetime.date.today().strftime('%Y%m%d')
        requester = QuoteRequester.objects.get_or_create(
            last_name=last_name,
            first_name=first_name,
            team=team,
            addressee=addressee
        )
        cart.requester = requester[0]
        cart.save()
        order_info_last = OrderInfo.objects.all().last()
        branch = 1
        if order_info_last is not None:
            old_number = order_info_last.number
            if today in old_number:
                old_branch = old_number.split('-')[1]
                branch += int(old_branch)
        number = today + '-' + str(branch)
        order_info = OrderInfo.objects.get_or_create(
            status=1,
            number=number,
            ticket=ticket,
            cart=cart,
        )
        context = {
            'orderinfo': order_info[0]
        }
        return render(request, 'quote/confirm.html', context)
    quoteitem_list = QuoteItem.objects.filter(worker=request.user, ordered=False)
    context = {
        'quoteitem_list': quoteitem_list,
        'count': len(quoteitem_list)
    }
    return render(request, 'quote/requester.html', context)
