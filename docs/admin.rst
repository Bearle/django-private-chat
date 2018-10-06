=====
Admin
=====

Application provides django admin intergration for ``Dialog`` and ``Message`` models.

In order to provide custom admin representation, first you have to unregister existing:

.. code-block:: python

    from django_private_chat.models import Dialog, Message
    admin.site.unregister(Dialog)
    admin.site.unregister(Message)

    // your example admin
    class DialogAdmin(admin.ModelAdmin):
        list_display = ('id',)
    admin.site.register(Dialog, DialogAdmin)
