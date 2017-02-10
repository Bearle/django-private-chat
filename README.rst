===================
django-private-chat
===================

.. image:: https://badge.fury.io/py/django-private-chat.svg
    :target: https://badge.fury.io/py/django-private-chat

.. image:: https://travis-ci.org/Bearle/django-private-chat.svg?branch=master
    :target: https://travis-ci.org/Bearle/django-private-chat

.. image:: https://codecov.io/gh/Bearle/django-private-chat/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Bearle/django-private-chat

Django one-to-one Websocket-based Asyncio-handled chat, developed by Bearle team

Documentation
-------------

The full documentation is at https://django-private-chat.readthedocs.io.

Quickstart
----------

Install django-private-chat::

    pip install django-private-chat

Migrate::

    python manage.py migrate django-private-chat

Note: you can use this package with or without uvloop, just run either

.. code-block:: python

    python manage.py run_chat_server

or run

.. code-block:: python

    python manage.py run_chat_server_uvloop



Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_private_chat.apps.DjangoPrivateChatConfig',
        ...
    )

Add the server & port for your asyncio server to settings:

.. code-block:: python

    CHAT_WS_SERVER_HOST = 'localhost'
    CHAT_WS_SERVER_PORT = 5002

It is possible to change messages datetime format using

.. code-block:: python

    DATETIME_FORMAT

Add django-private-chat's URL patterns:

.. code-block:: python

    from django_private_chat import urls as django_private_chat_urls


    urlpatterns = [
        ...
        url(r'^', include(django_private_chat_urls)),
        ...
    ]


Now you can start a dialog using ::

    /dialogs/some_existing_username



Features
--------

* Uses current app model (get_user_model() and settings.AUTH_USER_MODEL)
* Translatable (uses ugettext and {% trans %} )
* One-to-one user chat
* Works using WebSockets
* Displays online/offline status
* Display typing/not typing status
* Soft deletable message model - be sure to keep messages to comply with message-keeping laws
* TODO: add a dialog to the list when new one started
* TODO: add user-not-found and other alerts
* TODO: possible Redis backend intergration


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
