from .base import *
from .hide_settings import *

SECRET_KEY = '&&^=#bzu73d()3=7e!aff89ach^n$%9br4@49inp%a&#u3noa0'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
	# use mysql
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'Stoqu',
		'USER': LOCAL_DB_USER,
		'PASSWORD': LOCAL_DB_PASS,
		'HOST': '127.0.0.1',
		'PORT': LOCAL_DB_PORT,
		'OPTIONS': {
			'charset': 'utf8mb4',
		}
	}
}


# 管理サイトのログイン機能を通常のログイン機能として使う
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'
