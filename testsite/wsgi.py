"""
WSGI config for testsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
from dj_static import Cling
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")

from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())
