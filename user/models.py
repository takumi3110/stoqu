from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, password, is_superuser, **extra_fields):
		if not username:
			raise ValueError('The given username must be set')
		username = self.model.normalize_username(username)
		user = self.model(username=username, is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_superuser(self, username, password, **extra_fields):
		return self._create_user(username, password, True, **extra_fields)


# 独自ユーザーモデルの作成
class User(AbstractBaseUser, PermissionsMixin):
	user_vali = UnicodeUsernameValidator()
	username = models.CharField(
		verbose_name='社員番号',
		max_length=200,
		unique=True,
		validators=[user_vali]
	)
	screenname = models.CharField(
		verbose_name='氏名',
		max_length=200,
		blank=True,
	)
	first_name = models.CharField(
		_('first name'),
		max_length=100,
		blank=True,
	)
	last_name = models.CharField(
		_('last name'),
		max_length=100,
		blank=True,
	)
	department = models.CharField(
		verbose_name='部署',
		max_length=255,
		default='[]'
	)
	email = models.EmailField(
		_('email address'),
		blank=True,
	)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
	)
	created_date = models.DateTimeField(
		verbose_name='登録日時',
		auto_now_add=True,
	)
	objects = UserManager()
	USERNAME_FIELD = 'username'

	def __str__(self):
		return self.screenname

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('user')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name

	def get_short_name(self):
		return self.last_name


class Group(models.Model):
	name = models.CharField(
		verbose_name='グループ名',
		max_length=255,
		unique=True
	)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'グループ'
		verbose_name_plural = 'グループ'


class Member(models.Model):
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
		verbose_name='所属グループ'
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='ユーザー'
	)

	def __str__(self):
		return f'{self.group.name}: {self.user}'

	class Meta:
		verbose_name = 'メンバー'
		verbose_name_plural = 'メンバー'


@receiver(models.signals.post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
	if created:
		group, create = Group.objects.get_or_create(name='一般ユーザー')
		Member.objects.create(
			group=group,
			user=instance
		)
