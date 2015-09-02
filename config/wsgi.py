"""
WSGI config for wayup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

from configurations import importer


dotenv.read_dotenv(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".env")
    )
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

importer.install()

application = get_wsgi_application()


from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
