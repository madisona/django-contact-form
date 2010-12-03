
from setuptools import setup

setup(
    name="django-project",
    version="0.1",
    description="Django contact form app using buildout",
    author="Aaron Madison",
    packages=('contact_form',),
    package_dir={'': 'src'},
    install_requires = (
        'django==1.3-alpha-1',       # commenting out... using django 1.3 alpha 1 for now
        'unittest2',
        'docutils',      # so we can use django admin documentation
        'mock',          # used for testing purposes
        'django-debug-toolbar',
#        'pyyaml',        # useful for fixtures and testing
#        'south',         # incredibly useful for database migrations
    ),
    dependency_links=('http://www.djangoproject.com/download/1.3-alpha-1/tarball/#egg=django-1.3-alpha-1',),
)
