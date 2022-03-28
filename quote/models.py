from django.db import models
from django.utils import timezone

from device.models import PCDetail
from user.models import User, Requester
from stock.models import BaseManager


class Item(models.Model):
    genre = models.CharField(
        verbose_name='ジャンル',
        max_length=100,
    )
    
    maker = models.CharField(
        verbose_name='メーカー',
        max_length=100
    )
    
    name = models.CharField(
        verbose_name='商品名',
        max_length=255
    )
    
    spec = models.TextField(
        verbose_name='仕様',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'{self.maker}:{self.name}'
    
    class Meta:
        verbose_name = 'アイテム'
        verbose_name_plural = 'アイテム'


class Destination(models.Model):
    name = models.CharField(
        verbose_name='依頼先',
        max_length=50
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '販社'
        verbose_name_plural = '販社'


class QuoteRequester(models.Model):
    last_name = models.CharField(
        verbose_name='姓',
        max_length=50
    )
    
    first_name = models.CharField(
        verbose_name='名',
        max_length=50
    )
    
    addressee = models.CharField(
        verbose_name='宛名',
        max_length=255,
    )
    
    team = models.CharField(
        verbose_name='所属',
        max_length=255
    )
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    class Meta:
        verbose_name = '依頼者'
        verbose_name_plural = '依頼者'


class QuoteItem(models.Model):
    objects = BaseManager()
    
    number = models.PositiveSmallIntegerField(
        verbose_name='番号',
        default=1
    )
    
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='アイテム'
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name='数量',
        default=1
    )
    
    registration_at = models.DateTimeField(
        verbose_name='入力日',
        null=True,
        blank=True
    )
    
    ordered = models.BooleanField(
        verbose_name='見積もり依頼済み',
        default=False,
    )
    
    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='見積もり作成者',
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.registration_at = timezone.now()
        super(QuoteItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.item.maker} {self.item.name}:{self.quantity}'
    
    class Meta:
        verbose_name = '見積もりアイテム'
        verbose_name_plural = '見積もりアイテム'


class OrderItem(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        verbose_name='販社名'
    )
    
    quote_item = models.ForeignKey(
        QuoteItem,
        on_delete=models.CASCADE,
        verbose_name='見積もりアイテム'
    )
    
    ordered = models.BooleanField(
        verbose_name='見積もり依頼済み',
        default=False,
    )
    
    ordered_at = models.DateTimeField(
        verbose_name='依頼日',
        null=True,
        blank=True
    )
    
    arrived = models.BooleanField(
        verbose_name='見積もり到着済み',
        default=False
    )
    
    arrived_at = models.DateTimeField(
        verbose_name='見積もり到着日',
        null=True,
        blank=True
    )
    
    delivered = models.BooleanField(
        verbose_name='見積もり提供済み',
        default=False
    )
    
    delivery_at = models.DateField(
        verbose_name='見積もり提供日',
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if self.ordered:
            self.ordered_at = timezone.now()
        else:
            self.ordered_at = None
        if self.arrived:
            self.arrived_at = timezone.now()
        else:
            self.arrived_at = None
        if self.delivered:
            self.delivery_at = timezone.now()
        else:
            self.delivery_at = None
        super(OrderItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.quote_item.item.name} {self.destination.name}'
    
    class Meta:
        verbose_name = '依頼アイテム'
        verbose_name_plural = '依頼アイテム'


class Cart(models.Model):
    objects = BaseManager()
    
    requester = models.ForeignKey(
        QuoteRequester,
        on_delete=models.CASCADE,
        verbose_name='依頼者',
        null=True,
        blank=True
    )
    
    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='依頼作成者'
    )
    
    quote_item = models.ManyToManyField(
        QuoteItem,
        verbose_name='依頼アイテム'
    )
    
    input_at = models.DateTimeField(
        verbose_name='入力日',
        null=True,
        blank=True
    )
    
    ordered = models.BooleanField(
        verbose_name='依頼済み',
        default=False,
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.input_at = timezone.now()
        super(Cart, self).save(*args, **kwargs)
    
    def __str__(self):
        count = len(self.quote_item.all())
        return f'{self.worker.screenname}({count}個のアイテム)'
    
    class Meta:
        verbose_name = 'カート'
        verbose_name_plural = 'カート'


class OrderInfo(models.Model):
    status_choice = (
        ('1', '新規依頼'),
        ('2', '未対応'),
        ('3', '作成依頼中'),
        ('4', '見積もり到着'),
        ('5', '提供完了')
    )
    
    objects = BaseManager()
    
    status = models.CharField(
        verbose_name='ステータス',
        max_length=10,
        choices=status_choice,
        default=1
    )
    
    number = models.CharField(
        verbose_name='受注番号',
        max_length=200
    )
    
    ticket = models.CharField(
        verbose_name='チケット番号',
        max_length=50,
        null=True,
        blank=True
    )
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='カート'
    )
    
    registration_at = models.DateTimeField(
        verbose_name='依頼登録日',
        null=True,
        blank=True
    )
    
    updated_at = models.DateTimeField(
        verbose_name='更新日',
        null=True,
        blank=True
    )
    
    finished = models.BooleanField(
        verbose_name='完了',
        default=False
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.registration_at = timezone.now()
        else:
            if self.finished is False:
                finish = 0
                for quote_item in self.cart.quote_item.all():
                    if quote_item.delivered:
                        finish += 1
                if finish == len(self.cart.quote_item.all()):
                    self.finished = True
        self.updated_at = timezone.now()
        super(OrderInfo, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = '見積もり内容'
        verbose_name_plural = '見積もり内容'
