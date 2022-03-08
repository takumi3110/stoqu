"""
WSGI config for stoqu project.

It exposes the WSGI callable as a modules-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stoqu.settings.production')

application = get_wsgi_application()
