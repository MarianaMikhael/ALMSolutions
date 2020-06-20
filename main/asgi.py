"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = Cling(get_asgi_application())
