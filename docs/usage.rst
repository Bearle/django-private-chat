=====
Usage
=====

To use django-private-chat in a project, add it to your `INSTALLED_APPS`:

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
