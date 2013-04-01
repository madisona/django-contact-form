Extensible contacts form implemented in class-based views. Forked from `django-contact-form`_

.. image:: https://travis-ci.org/futurecolors/django-contact-form.png?branch=master
    :target: https://travis-ci.org/futurecolors/django-contact-form

.. image:: https://coveralls.io/repos/futurecolors/django-contact-form/badge.png?branch=master
    :target: https://coveralls.io/r/futurecolors/django-contact-form/

.. _django-contact-form: https://github.com/madisona/django-contact-form

Tested with Django >=1.4.

Uses django-templated-email to send mail by default.


Install
=======

Add ``'contact_form'`` to your ``INSTALLED_APPS``::

    # settings.py
    INSTALLED_APPS = (
        ...
        'contact_form',
        ...
    )

Add application urs to your urlconf. Example::

    # urls.py
    urlpatterns += patterns('',
        (r'', include('contact_form.urls')),
    )
