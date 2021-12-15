from .base import *
from .hide_settings import *

SECRET_KEY = '&&^=#bzu73d()3=7e!aff89ach^n$%9br4@49inp%a&#u3noa0'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
	# use mysql
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'Quote',
		'USER': DEPLOY_DB_USER,
		'PASSWORD': DEPLOY_DB_PASS,
		'HOST': 'localhost',
		'PORT': DEPLOY_DB_PORT,
		'OPTIONS': {
			'charset': 'utf8mb4',
		}
	}
}

# 管理サイトのログイン機能を通常のログイン機能として使う
LOGIN_URL = '/quote/admin/login/'
LOGIN_REDIRECT_URL = '/quote/'
LOGOUT_REDIRECT_URL = '/quote/'
