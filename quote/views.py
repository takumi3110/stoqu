from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse

from rest_framework import viewsets
from bootstrap_modal_forms.generic import BSModalCreateView

from .models import Item, QuoteItem, Destination, QuoteRequester, OrderItem, Cart, OrderInfo
from device.models import PC, PCDetail, Storage, CPU
from .serializers import QuoteItemSerializer
from .filters import QuoteItemFilter
from .forms import DestinationCreateBSModalForm

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
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
                spec_text = 'cpu:{}\nメモリ:{}GB\nストレージ:SSD{}GB\nテンキー:{}\n指紋認証:あり' \
                    .format(cpu, memory, storage, ten_key)
            else:
                spec_text = 'cpu:{}\nメモリ:{}GB\nストレージ:SSD{}GB\n'.format(cpu, memory, storage)
            if lanscope == 'true':
                license_name = 'Lanscope Cat'
                license_maker = 'Lanscope'
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
            spec_text = '{}\n{}インチ\nワイドモニター\nノングレア\n{}'.format(spec, size, detail)
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
                    OrderItem.objects.update_or_create(
                        destination_id=post_name,
                        quote_item=quote_item,
                        ordered=False,
                        arrived=False,
                        delivered=False
                    )
                    cart[0].quote_item.add(quote_item)
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
        quoteitem_list = QuoteItem.objects.filter(worker=request.user, ordered=False)
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
        # cart.ordered = True
        # cart.save()
        order_info_all = OrderInfo.objects.all()
        order_info_last = order_info_all.last()
        branch = 1
        order_info_filter = OrderInfo.objects.filter(ticket=ticket, cart=cart)
        if order_info_last is not None:
            old_number = order_info_last.number
            if today in old_number and not order_info_filter:
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
            'orderinfo': order_info[0],
            'quoteitem_list': quoteitem_list
        }
        return render(request, 'quote/confirm.html', context)
    quoteitem_list = QuoteItem.objects.filter(worker=request.user, ordered=False)
    context = {
        'quoteitem_list': quoteitem_list,
        'count': len(quoteitem_list)
    }
    return render(request, 'quote/requester.html', context)


class OrderInfoView(LoginRequiredMixin, ListView):
    model = OrderInfo
    template_name = 'quote/orderinfo.html'


class OrderInfoMyView(LoginRequiredMixin, ListView):
    model = OrderInfo
    template_name = 'quote/orderinfo_my.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(OrderInfoMyView, self).get_queryset()
        qs = queryset.filter(cart__worker=self.request.user).order_by('-pk')
        return qs


class OrderInfoDetailView(LoginRequiredMixin, DetailView):
    model = OrderInfo
    template_name = 'quote/orderinfo_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(OrderInfoDetailView, self).get_context_data(**kwargs)
        quote_item_list = context['orderinfo'].cart.quote_item.all()
        orderitem_list = []
        orderitem_dict = {}
        for quote_item in quote_item_list:
            order_item_filter = OrderItem.objects.filter(quote_item=quote_item)
            orderitem_dict[quote_item.item] =[]
            for order_item in order_item_filter:
                orderitem_list.append(order_item)
                orderitem_dict[quote_item.item].append(order_item)
        status = {}
        for choice in context['orderinfo'].status_choice:
            status[int(choice[0])] = choice[1]
        context['orderitem_dict'] = orderitem_dict
        context['status'] = status
        context['active_status'] = int(context['orderinfo'].status)
        return context


def create_pdf_data(quote_item, order_info):
    number = quote_item.number
    ticket = str(order_info.ticket) + '-' + str(number)
    genre = quote_item.item.genre
    maker = quote_item.item.maker
    name = quote_item.item.name
    quantity = quote_item.quantity
    spec = quote_item.item.spec
    addressee = order_info.cart.requester
    order = [ticket, genre, maker, name, quantity, spec, addressee]
    pdf_data = {
        'order': order,
        'length': len(spec)
    }
    return pdf_data


def create_row_heights(length):
    heights = []
    if length == 0:
        heights.append(20 * mm)
    else:
        size = length * 6
        heights.append(size * mm)
    return heights


def create_col_width(length):
    # (30 * mm, 25 * mm, 25 * mm, 50 * mm, 15 * mm, 50 * mm, 80 * mm)
    width = []
    return width
    

class PDFBaseView(View):
    def get(self, request, *args, **kwargs):
        title = '■プレステージ・インターナショナル　秋田BPOキャンパス　見積依頼'
        font_name = 'HeiseiKakuGo-W5'
        is_bottomup = False
        response = HttpResponse(status=200, content_type='application/pdf')
        # 日本語が使えるゴシック体のフォントを設定
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))
        size = landscape(A4)
        # pdfを描く場所を作成。位置を決める原点は左上にする。(bottomup)デフォルトは左下
        doc = canvas.Canvas(response, pagesize=size, bottomup=is_bottomup)
        # pdfのタイトルを設定
        doc.setTitle(title)
        # フォントを設定
        doc.setFont(font_name, 10)
        # pdf上にもタイトルとしてしようしたクラス名を表示する
        doc.drawString(10 * mm, 15 * mm, title)
        # 即ダウンロードしたいときはattachmentをつける
        # response['Content-Disposition'] = 'filename="{}"'.format(filename)
        header = ['管理番号', '機器', 'メーカー', '型式', '数量', '仕様/構成', '宛名']
        filename = self.pdf_draw(doc, kwargs['pk'], header)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


class CreatePdf(PDFBaseView):
    def create_pdf_style(self, doc, data, row_heights):
        top = 5 * mm
        left = 20 * mm
        heights = tuple(row_heights)
        widths = (30 * mm, 25 * mm, 25 * mm, 50 * mm, 15 * mm, 50 * mm, 80 * mm)
        table = Table(data, colWidths=widths, rowHeights=heights)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.font_name, 10),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
            ('BACKGROUND', (0, 0), (0, -2), colors.lightyellow)
        ]))
        table.wrapOn(doc, top, left)
        table.drawOn(doc, top, left)
    
    def pdf_draw(self, doc, pk, header):
        data = [header]
        order_item = OrderItem.objects.get(pk=pk)
        order_info = OrderInfo.objects.get(cart__order_item=order_item)
        pdf_data = create_pdf_data(order_item, order_info)
        order = pdf_data['order']
        length = pdf_data['length']
        data.append(order)
        data.reverse()
        row_heights = [10 * mm]
        for h in create_row_heights(length):
            row_heights.append(h)
        row_heights.reverse()
        create_pdf_style(self, doc, data, row_heights)
        filename = order[0] + '_見積作成依頼書.pdf'
        doc.save()
        return filename


class AllCreatePdf(PDFBaseView):
    def create_pdf_style(self, doc, data, row_heights):
        top = 5 * mm
        left = 20 * mm
        heights = tuple(row_heights)
        widths = (30 * mm, 25 * mm, 25 * mm, 50 * mm, 15 * mm, 50 * mm, 80 * mm)
        table = Table(data, colWidths=widths, rowHeights=heights)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.font_name, 10),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
            ('BACKGROUND', (0, 0), (0, -2), colors.lightyellow)
        ]))
        table.wrapOn(doc, top, left)
        table.drawOn(doc, top, left)
    
    def pdf_draw(self, doc, pk, header):
        data = []
        row_heights = [10 * mm]
        order_info = OrderInfo.objects.get(pk=pk)
        quote_item_list = order_info.cart.quote_item.all()
        order_info.cart.ordered = True
        order_info.cart.save()
        for quote_item in quote_item_list:
            order_item = OrderItem.objects.get(quote_item=quote_item)
            order_item.ordered = True
            order_item.save()
            pdf_data = create_pdf_data(quote_item, order_info)
            order = pdf_data['order']
            length = pdf_data['length']
            data.append(order)
            for h in create_row_heights(length):
                row_heights.append(h)
        data.insert(0, header)
        data.reverse()
        row_heights.reverse()
        create_pdf_style(self, doc, data, row_heights)
        filename = str(order_info.ticket) + '_見積作成依頼書.pdf'
        doc.save()
        return filename
