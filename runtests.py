#!/usr/bin/env python
import sys
from optparse import OptionParser
from django.conf import settings

def get_safe_settings(settings_module):
    """
    setup.py test and the multiprocessing module tend
    to fight. Since lettuce.django uses the multiprocessing
    module we do not want to include that when running unit tests with
    setup.py test because it causes an error every time, even though
    the tests run fine.

    Here is the exception that will occur after the tests finish.

    Traceback (most recent call last):
      File "/usr/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
        func(*targs, **kargs)
      File "/usr/lib/python2.7/multiprocessing/util.py", line 284, in _exit_function
        info('process shutting down')
    TypeError: 'NoneType' object is not callable

    For more details see:
        http://comments.gmane.org/gmane.comp.python.distutils.devel/11688
    """

    installed_apps = list(settings_module.INSTALLED_APPS)
    if 'lettuce.django' in installed_apps:
        installed_apps.pop(installed_apps.index('lettuce.django'))
        settings_module.INSTALLED_APPS = installed_apps
    return settings_module

if not settings.configured:
    #load django settings from example project for tests
    from example import settings as example_settings
    safe_settings = get_safe_settings(example_settings)

    settings.configure(**safe_settings.__dict__)

#This import must come after settings config
from django.test.simple import run_tests

def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['contact_form']

    failures = run_tests(test_args, verbosity=kwargs.get('verbosity', 1), interactive=kwargs.get('interactive', False), failfast=kwargs.get('failfast'))
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)