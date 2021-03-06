from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

type_choice = (
	('1', 'SSD'),
	('2', 'HDD')
)

category_choice = (
	('note', 'ノートPC'),
	('desktop', 'デスクトップPC'),
	('mini', 'ミニPC')
)


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
		verbose_name='世代',
		validators=[
			MaxValueValidator(99)
		]
	)
	
	latest = models.BooleanField(
		verbose_name='最新',
		default=False
	)

	def __str__(self):
		return f'{self.maker} {self.name} 第{self.gen}世代'

	class Meta:
		verbose_name = 'CPU'
		verbose_name_plural = 'CPU'


class Storage(models.Model):
	type = models.CharField(
		verbose_name='タイプ',
		max_length=6,
		choices=type_choice,
		default=1
	)

	size = models.PositiveSmallIntegerField(
		verbose_name='容量(GB)',
	)

	def __str__(self):
		return f'{self.get_type_display()} {self.size}GB'

	class Meta:
		verbose_name = 'ストレージ'
		verbose_name_plural = 'ストレージ'


class PC(models.Model):
	category = models.CharField(
		verbose_name='カテゴリー',
		max_length=8,
		choices=category_choice,
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
	
	img = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	sub_img1 = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	sub_img2 = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	sub_img3 = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	sub_img4 = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	sub_img5 = models.ImageField(
		upload_to='images/pc/',
		null=True,
		blank=True
	)
	
	url = models.URLField(
		null=True,
		blank=True
	)

	def __str__(self):
		return f'{self.maker} {self.name}'

	class Meta:
		verbose_name = 'PC'
		verbose_name_plural = 'PC'


class PCDetail(models.Model):
	pc = models.ForeignKey(
		PC,
		on_delete=models.CASCADE,
		verbose_name='PC',
	)

	cpu = models.ForeignKey(
		CPU,
		on_delete=models.CASCADE,
		verbose_name='CPU',
	)

	memory = models.PositiveSmallIntegerField(
		verbose_name='メモリー(GB)',
		null=True,
		blank=True
	)

	storage = models.ForeignKey(
		Storage,
		on_delete=models.CASCADE,
		verbose_name='ストレージ',
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
		blank=True
	)

	fingerprint = models.BooleanField(
		verbose_name='指紋認証',
		blank=True
	)

	numpad = models.BooleanField(
		verbose_name='テンキー',
		default=False,
		blank=True
	)

	lan = models.BooleanField(
		verbose_name='有線LANポート',
		default=False,
		blank=True
	)

	usb = models.PositiveSmallIntegerField(
		verbose_name='USBポート',
		null=True,
		blank=True,
		validators=[
			MaxValueValidator(10)
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

	remarks = models.TextField(
		verbose_name='備考',
		null=True,
		blank=True
	)

	def save(self, *args, **kwargs):
		if self.memory is None:
			if self.pc.category == 2:
				self.memory = 16
			else:
				self.memory = 8
		if self.pc.category == 'note':
			self.camera = True
			self.fingerprint = True
			if self.size < 15:
				self.numpad = False
			else:
				self.numpad = True
		else:
			self.camera = False
			self.fingerprint = False
			self.lan = True
		super(PCDetail, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.pc.maker} {self.pc.name}'

	class Meta:
		verbose_name = 'PC詳細'
		verbose_name_plural = 'PC詳細'
