from django.db import models

from device.models import PCDetail


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
		verbose_name='合計金額'
	)

	quantity = models.PositiveSmallIntegerField(
		verbose_name='在庫数',
		null=True,
		blank=True
	)

	option = models.ManyToManyField(
		Option,
		verbose_name='オプション',
		blank=True
	)

	base = models.ForeignKey(
		Base,
		on_delete=models.CASCADE,
		verbose_name='在庫拠点',
	)

	delivery_date = models.DateField(
		verbose_name='納品日',
		null=True,
		blank=True
	)

	remarks = models.TextField(
		verbose_name='備考',
		null=True,
		blank=True
	)

	def __str__(self):
		return f'{self.item.pc.maker}{self.item.pc.name}'

	class Meta:
		verbose_name = '貯蔵品'
		verbose_name_plural = '貯蔵品'
