"""
WSGI config for d06siims project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd06siims.settings')

application = get_wsgi_application()

<<<<<<< HEAD
app = application
=======
app = application
>>>>>>> 79e180fa5d32da73d97f852db285b72c1061b136
