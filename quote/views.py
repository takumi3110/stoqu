from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

from rest_framework import viewsets
from bootstrap_modal_forms.generic import BSModalCreateView

from .models import Item, QuoteItem, Destination, QuoteRequester
from device.models import PC, PCDetail, Storage, CPU
from .serializers import QuoteItemSerializer
from .filters import QuoteItemFilter
from .forms import DestinationCreateBSModalForm


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
    if request.method == 'post':
        return redirect('quote:register_destination')
    destination = Destination.objects.all()
    quoteitem_list = QuoteItem.objects.filter(worker=request.user, ordered=False)
    context = {
        'destination_list': destination,
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
    return render(request, 'quote/confirm.html')
