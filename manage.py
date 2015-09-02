#!/usr/bin/env python
import dotenv
import os
import sys
from configurations import importer

dotenv.read_dotenv()



if __name__ == "__main__":
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # NOTE(Ahmed): https://github.com/jezdez/django-configurations/issues/25
    importer.install()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
