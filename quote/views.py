from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from .models import Item, QuoteItem
from device.models import PC, PCDetail, Storage, CPU


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
        if maker == 'none':
            maker = 'メーカー問わず'
        if genre == 'pc':
            category = request.POST['category']
            ten_key = request.POST['ten_key']
            cpu = request.POST['cpu']
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
        elif genre == 'display':
            genre = 'ディスプレイ'
            size = request.POST['size']
            if spec == 'normal':
                spec_text = 'FHD\n{}インチ\nワイドモニター'.format(size)
            elif spec == 'wqhd':
                spec_text = 'WQHD\n{}インチ\nワイドモニター'.format(size)
            elif spec == '4k':
                spec_text = '4k\n{}インチ\nワイドモニター'.format(size)
        elif genre == 'others':
            genre = '周辺機器'
            name = request.POST['name']
            spec_text = spec
        item = Item.objects.get_or_create(
            genre=genre,
            maker=maker,
            name=name,
            spec=spec_text
        )
        quote_item_filter = QuoteItem.objects.filter(worker=request.user, ordered=False, delivered=False)
        if quote_item_filter:
            last_item = quote_item_filter.last()
            for quote in quote_item_filter:
                if item[0] == quote.item:
                    quote.quantity += int(quantity)
                else:
                    QuoteItem.objects.create(
                        number=last_item.number + 1,
                        item=item[0],
                        quantity=quantity,
                        worker=request.user
                    )
                quote.save()
        else:
            QuoteItem.objects.create(
                number=1,
                item=item[0],
                quantity=quantity,
                worker=request.user
            )
        new_quote_item = QuoteItem.objects.filter(worker=request.user, ordered=False, delivered=False)
        context['quoteitem_list'] = new_quote_item
        return redirect('quote:item_list')
    else:
        return render(request, 'quote/order.html', context)


class QuoteItemList(LoginRequiredMixin, ListView):
    model = QuoteItem
    template_name = 'quote/cart.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(QuoteItemList, self).get_queryset()
        qs = queryset.filter(worker=self.request.user, ordered=False)
        return qs
