from django.db import models

from device.models import PCDetail
from user.models import User


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
		verbose_name = 'オプション'
		verbose_name_plural = 'オプション'


class Base(models.Model):
	name = models.CharField(
		verbose_name='拠点名',
		max_length=50
	)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '拠点'
		verbose_name_plural = '拠点'


class StorageItem(models.Model):
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

	delivery_at = models.DateField(
		verbose_name='納品日',
		null=True,
		blank=True
	)

	remarks = models.TextField(
		verbose_name='備考',
		null=True,
		blank=True
	)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.total_price = self.price
		for option in self.option.all():
			self.total_price += option.price
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.item.pc.maker}{self.item.pc.name}'

	class Meta:
		verbose_name = '貯蔵品'
		verbose_name_plural = '貯蔵品'


class OrderItem(models.Model):
	storage_item = models.ForeignKey(
		StorageItem,
		on_delete=models.CASCADE,
		verbose_name='貯蔵品'
	)

	quantity = models.PositiveSmallIntegerField(
		verbose_name='数量',
	)

	ordered = models.BooleanField(
		verbose_name='確保済み',
		default=False
	)

	def __str__(self):
		return f'{self.storage_item.item.pc.maker} {self.storage_item.item.pc.name} × {self.quantity}'

	class Meta:
		verbose_name = '確保アイテム'
		verbose_name_plural = '確保アイテム'


class StorageCart(models.Model):
	requester = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='依頼者'
	)

	order_item = models.ManyToManyField(
		OrderItem,
		verbose_name='確保アイテム',
	)

	ordered = models.BooleanField(
		default=False
	)

	def __str__(self):
		return self.requester.screenname

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

	def __str__(self):
		return f'{self.last_name}{self.first_name}'

	class Meta:
		verbose_name = '承認者情報'
		verbose_name_plural = '承認者情報'


class OrderInfo(models.Model):
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
		User,
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
		auto_now=True
	)

	ordered = models.BooleanField(
		verbose_name='依頼済み'
	)

	def __str__(self):
		return f'{self.number}'

	class Meta:
		verbose_name = '依頼内容'
		verbose_name_plural = '依頼内容'
