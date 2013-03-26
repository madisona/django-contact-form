from os.path import join, abspath, dirname

PROJECT_DIR = abspath(dirname(__file__))
TEMPLATE_DIRS = (
    join(PROJECT_DIR, 'templates'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6kfuaep$0j)5*b-zodi+p)x*xl$=27@s@queywbp_$_l4f#3a+'

ROOT_URLCONF = 'example.urls'
INSTALLED_APPS = (
    'contact_form',
)

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
ADMINS = (
    ('Joe Smith', 'joe.smith@example.com'),
)

MANAGERS = ADMINS