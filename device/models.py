from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CPU(models.Model):
	maker = models.CharField(
		verbose_name='メーカー',
		max_length=20,
		default='Intel'
	)

	name = models.CharField(
		max_length=50
	)

	gen = models.PositiveSmallIntegerField(
		verbose_name='世代'
	)

	def __str__(self):
		return f'{self.maker} {self.name} 第{self.gen}世代'

	class Meta:
		verbose_name = 'CPU'
		verbose_name_plural = 'CPU'


class Storage(models.Model):
	type = models.CharField(
		verbose_name='タイプ',
		max_length=5
	)

	size = models.PositiveSmallIntegerField(
		verbose_name='容量(GB)',
	)

	def __str__(self):
		return f'{self.type} {self.size}GB'

	class Meta:
		verbose_name = 'ストレージ'
		verbose_name_plural = 'ストレージ'


class PCSpec(models.Model):
	memory_choice = (
		('1', '8'),
		('2', '16'),
		('3', '24'),
		('4', '32')
	)

	cpu = models.ForeignKey(
		CPU,
		on_delete=models.CASCADE,
		verbose_name='CPU',
	)

	memory = models.CharField(
		verbose_name='メモリー(GB)',
		max_length=5,
		choices=memory_choice
	)

	storage = models.ForeignKey(
		Storage,
		on_delete=models.CASCADE,
		verbose_name='ストレージ'
	)

	size = models.PositiveSmallIntegerField(
		verbose_name='サイズ(インチ)',
		null=True,
		blank=True,
		validators=[
			MinValueValidator(12),
			MaxValueValidator(16)
		]
	)

	camera = models.BooleanField(
		verbose_name='webカメラ',
		null=True,
		blank=True
	)

	fingerprint = models.BooleanField(
		verbose_name='指紋認証',
		null=True,
		blank=True
	)

	numpad = models.BooleanField(
		verbose_name='テンキー',
		null=True,
		blank=True
	)

	lan = models.BooleanField(
		verbose_name='有線LANポート',
		null=True,
		blank=True
	)

	usb = models.PositiveSmallIntegerField(
		verbose_name='USBポート',
		null=True,
		blank=True,
		validators=[
			MaxValueValidator(4)
		]
	)

	hdmi = models.PositiveSmallIntegerField(
		verbose_name='HDMI',
		null=True,
		blank=True,
		validators=[
			MaxValueValidator(4)
		]
	)

	vga = models.PositiveSmallIntegerField(
		verbose_name='VGA',
		null=True,
		blank=True,
		validators=[
			MaxValueValidator(2)
		]
	)

	def __str__(self):
		return f'{self.cpu} {self.storage} {self.memory}'

	class Meta:
		verbose_name = 'スペック(PC)'
		verbose_name_plural = 'スペック(PC)'


class PC(models.Model):
	category_choice = (
		('1', 'ノート'),
		('2', 'デスクトップ'),
		('3', 'ミニPC')
	)

	category = models.CharField(
		verbose_name='カテゴリー',
		max_length=5,
		choices=category_choice
	)

	maker = models.CharField(
		verbose_name='メーカー',
		max_length=50,
	)

	name = models.CharField(
		verbose_name='製品名',
		max_length=100,
	)

	model_number = models.CharField(
		verbose_name='型番',
		max_length=100,
		null=True,
		blank=True
	)

	def __str__(self):
		return f'{self.maker} {self.name}'


class Item(models.Model):
	pc = models.ForeignKey(
		PC,
		on_delete=models.CASCADE,
		verbose_name='PC',
	)

	spec = models.ForeignKey(
		PCSpec,
		on_delete=models.CASCADE,
		verbose_name='スペック'
	)

	remarks = models.TextField(
		verbose_name='備考',
		null=True,
		blank=True
	)

	def __str__(self):
		return self.pc

	class Meta:
		verbose_name = 'Item'
		verbose_name_plural = 'Item'
