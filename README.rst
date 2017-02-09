=============================
django-private-chat
=============================

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

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_private_chat.apps.DjangoPrivateChatConfig',
        ...
    )

Add django-private-chat's URL patterns:

.. code-block:: python

    from django_private_chat import urls as django_private_chat_urls


    urlpatterns = [
        ...
        url(r'^', include(django_private_chat_urls)),
        ...
    ]

Features
--------

* TODO

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
