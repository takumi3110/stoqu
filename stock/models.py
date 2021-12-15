from django.db import models

from device.models import Item


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


class Storage(models.Model):
	order_number = models.CharField(
		verbose_name='発注番号',
		max_length=100
	)


