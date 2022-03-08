from django.db import models
from django.utils import timezone

import datetime

from device.models import PCDetail
from user.models import User, Base, Requester


class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Option(models.Model):
    maker = models.CharField(
        verbose_name='メーカー',
        max_length=100
    )
    
    name = models.CharField(
        verbose_name='製品名',
        max_length=200
    )
    
    price = models.PositiveIntegerField(
        verbose_name='金額(円)'
    )
    
    quantity = models.PositiveSmallIntegerField(
        verbose_name='在庫数'
    )
    
    remarks = models.TextField(
        verbose_name='備考',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'{self.maker}{self.name}'
    
    class Meta:
        verbose_name = '付属品'
        verbose_name_plural = '付属品'


class StorageItem(models.Model):
    objects = BaseManager()
    
    order_number = models.CharField(
        verbose_name='発注番号',
        max_length=100
    )
    
    item = models.ForeignKey(
        PCDetail,
        on_delete=models.CASCADE,
        verbose_name='在庫PC'
    )
    
    price = models.PositiveIntegerField(
        verbose_name='本体価格'
    )
    
    quantity = models.PositiveSmallIntegerField(
        verbose_name='在庫数',
        null=True,
        blank=True
    )
    
    option = models.ManyToManyField(
        Option,
        verbose_name='付属品',
        blank=True
    )
    
    total_price = models.PositiveIntegerField(
        verbose_name='合計金額',
        null=True,
        blank=True
    )
    
    base = models.ForeignKey(
        Base,
        on_delete=models.CASCADE,
        verbose_name='在庫拠点',
    )
    
    registration_at = models.DateField(
        verbose_name='登録日',
        null=True,
        blank=True
    )
    
    remarks = models.TextField(
        verbose_name='備考',
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if self.registration_at is None and not self.id:
            self.registration_at = timezone.now()
        self.total_price = self.price
        super(StorageItem, self).save(*args, **kwargs)
        if self.id is not None:
            for option in self.option.all():
                self.total_price += option.price
        super(StorageItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.item} ({self.base})'
    
    class Meta:
        verbose_name = '貯蔵品'
        verbose_name_plural = '貯蔵品'


class KittingPlan(models.Model):
    objects = BaseManager()
    
    kitting_choice = (
        ('標準', '標準'),
        ('お急ぎ便', 'お急ぎ便')
    )
    name = models.CharField(
        verbose_name='プラン名',
        max_length=10,
        choices=kitting_choice,
        default='標準'
    )
    
    price = models.PositiveSmallIntegerField(
        verbose_name='金額',
    )
    
    due = models.PositiveSmallIntegerField(
        verbose_name='納期',
        default=7
    )
    
    def __str__(self):
        return f'{self.name} {self.price}円'
    
    class Meta:
        verbose_name = 'キッティング価格'
        verbose_name_plural = 'キッティング価格'


class OrderItem(models.Model):
    objects = BaseManager()
    
    storage_item = models.ForeignKey(
        StorageItem,
        on_delete=models.CASCADE,
        verbose_name='貯蔵品'
    )
    
    quantity = models.PositiveSmallIntegerField(
        verbose_name='数量',
        default=1
    )
    
    ordered = models.BooleanField(
        verbose_name='確保済み',
        default=False
    )
    
    kitting_plan = models.ForeignKey(
        KittingPlan,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    price = models.PositiveIntegerField(
        verbose_name='合計金額',
        null=True,
        blank=True
    )
    
    due_at = models.DateField(
        verbose_name='納品予定日',
        null=True,
        blank=True
    )
    
    requester = models.ForeignKey(
        Requester,
        on_delete=models.CASCADE,
        verbose_name='依頼者',
    )
    
    def save(self, *args, **kwargs):
        item_price = self.storage_item.total_price
        price = item_price * self.quantity
        kitting_plan = self.kitting_plan
        if kitting_plan is not None:
            now = datetime.datetime.now()
            hour = now.hour
            day = kitting_plan.due
            over_day = day + 1
            if hour >= 17:
                date = datetime.date.today() + datetime.timedelta(days=over_day)
            else:
                date = datetime.date.today() + datetime.timedelta(days=day)
            self.due_at = date
            self.price = price + kitting_plan.price
        else:
            self.price = price
        super(OrderItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.storage_item} × {self.quantity}'
    
    class Meta:
        verbose_name = '確保アイテム'
        verbose_name_plural = '確保アイテム'


class StorageCart(models.Model):
    objects = BaseManager()
    
    requester = models.ForeignKey(
        Requester,
        on_delete=models.CASCADE,
        verbose_name='依頼者'
    )
    
    order_item = models.ManyToManyField(
        OrderItem,
        verbose_name='確保アイテム',
    )
    
    price = models.PositiveIntegerField(
        verbose_name='合計金額（税込み）',
        null=True,
        blank=True
    )
    
    tax_price = models.PositiveSmallIntegerField(
        verbose_name='消費税',
        null=True,
        blank=True
    )
    
    ordered = models.BooleanField(
        default=False
    )
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.price = 0
            subtotal = 0
            tax = 0.1
            self.tax_price = 0
            for item in self.order_item.all():
                subtotal += item.storage_item.total_price * item.quantity
                if item.kitting_plan is not None:
                    subtotal += item.kitting_plan.price
            self.tax_price += round(subtotal * tax)
            self.price += subtotal + self.tax_price
        super(StorageCart, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.requester.user.screenname
    
    class Meta:
        verbose_name = '貯蔵品カート'
        verbose_name_plural = '貯蔵品カート'


class Approve(models.Model):
    last_name = models.CharField(
        verbose_name='姓',
        max_length=32
    )
    
    first_name = models.CharField(
        verbose_name='名',
        max_length=32,
    )
    
    dept_code = models.PositiveSmallIntegerField(
        verbose_name='部門コード'
    )
    
    dept_name = models.CharField(
        verbose_name='部門名',
        max_length=255
    )
    
    requester = models.ForeignKey(
        Requester,
        on_delete=models.CASCADE,
        verbose_name='依頼者',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    class Meta:
        verbose_name = '承認者情報'
        verbose_name_plural = '承認者情報'


class OrderInfo(models.Model):
    status_choices = (
        ('1', '準備中'),
        ('2', '確保済み'),
        ('3', 'キッティング中'),
        ('4', 'キッティング完了'),
        ('5', '納品済み')
    )
    
    objects = BaseManager()
    
    status = models.CharField(
        verbose_name='ステータス',
        max_length=2,
        choices=status_choices,
        default=1
    )
    
    number = models.CharField(
        verbose_name='受注番号',
        max_length=100
    )
    
    ticket = models.PositiveIntegerField(
        verbose_name='チケット番号',
        null=True,
        blank=True
    )
    
    storage_cart = models.ForeignKey(
        StorageCart,
        on_delete=models.CASCADE,
        verbose_name='カート'
    )
    
    approve = models.ForeignKey(
        Approve,
        on_delete=models.CASCADE,
        verbose_name='承認者情報'
    )
    
    requester = models.ForeignKey(
        Requester,
        on_delete=models.CASCADE,
        verbose_name='依頼者'
    )
    
    contact_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='担当者',
        null=True,
        blank=True,
        related_name='contact_user'
    )
    
    ordered_at = models.DateTimeField(
        verbose_name='依頼日',
        null=True,
        blank=True
    )
    
    updated_at = models.DateTimeField(
        verbose_name='更新日',
        null=True,
        blank=True
    )
    
    completed_delivery = models.BooleanField(
        verbose_name='納品済み',
        default=False
    )
    
    delivery_at = models.DateTimeField(
        verbose_name='納品日',
        null=True,
        blank=True
    )
    
    due_at = models.DateField(
        verbose_name='納品予定日',
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.ordered_at = timezone.now()
        self.updated_at = timezone.now()
        if self.delivery_at is not None:
            self.completed_delivery = True
        due = []
        for item in self.storage_cart.order_item.all():
            due.append(item.due_at)
        due.sort()
        self.due_at = due[-1]
        super(OrderInfo, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.number}'
    
    class Meta:
        verbose_name = '依頼内容'
        verbose_name_plural = '依頼内容'
