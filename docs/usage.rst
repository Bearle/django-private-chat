=====
Usage
=====

To use django-private-chat in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
       'django_private_chat',
        ...
    )

Add the server & port for your asyncio server to settings:

.. code-block:: python

    CHAT_WS_SERVER_HOST = 'localhost'
    CHAT_WS_SERVER_PORT = 5002
    CHAT_WS_SERVER_PROTOCOL = 'ws'

Add django-private-chat's URL patterns:

.. code-block:: python

    from django_private_chat import urls as django_private_chat_urls


    urlpatterns = [
        ...
        url(r'^', include(django_private_chat_urls)),
        ...
    ]
    
or

.. code-block:: python

    urlpatterns = [
        ...
        path('', include(django_private_chat.urls)),
        ...
    ]


Add

.. code-block:: python

    {% block css %}{% endblock css %}
    {% block content %}{% endblock content %}
    {% block extra_js %}{% endblock extra_js %}

to your base template

Migrate::

    python manage.py migrate django_private_chat

Now start the chat server:

.. code-block:: python

    python manage.py run_chat_server
