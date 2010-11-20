
from setuptools import setup

setup(
    name="django-project",
    version="0.1",
    description="Django app using buildout",
    author="Aaron Madison",

    package_dir={'': 'src'},
    install_requires = (
#        'django',       # commenting out... using django 1.3 alpha 1 for now
        'mock',          # used for testing purposes
        'django-debug-toolbar',
#        'pyyaml',        # useful for fixtures and testing
#        'south',         # incredibly useful for database migrations
#        'coverage',      # useful for continuous integration, tells how much of code is covered by tests 
#        'clonedigger',   # useful for continuous integration, looks for duplicate chunks of code
#        'unittest-xml-reporting', # useful for continuous integration, makes nice test results
#        'pylint',        # useful for continuous integration, looks at code quality
    ),
)
