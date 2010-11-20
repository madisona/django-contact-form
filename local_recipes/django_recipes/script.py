
import os
import zc

class Recipe(object):

    def __init__(self, buildout, name, options):
        print dir(zc)
        self.egg = zc.recipe.egg.Egg(buildout, 'django_recipes', options)
        self.buildout, self.name, self.options = buildout, name, options

        options['bin-directory'] = buildout['buildout']['bin-directory']
        self.extra_paths = []
        if 'extra-paths' in options:
            self.extra_paths = [path for path in options['extra-paths'].split(' ')]

    def install(self):
        self.options.setdefault('wsgi', "false")

        requirements, ws = self.egg.working_set()

        script_paths = []

        # create manage.py script
        script_paths.extend(self.create_manage_script(self.extra_paths, ws))
        if self.options['wsgi'].lower() == "true":
            script_paths.extend(self.create_wsgi_script(self.extra_paths, ws))

        return script_paths

    def update(self):
        self.install()
    
    def create_manage_script(self, extra_paths, ws):
        file_name = "manage.py"
        template = manage_template
        return self.create_script(self.extra_paths, ws, file_name, template)

    def create_wsgi_script(self, extra_paths, ws):
        file_name = "django.wsgi"
        template = wsgi_template
        return self.create_script(self.extra_paths, ws, file_name, template)

    def create_script(self, extra_paths, ws, file_name, template):
        # save off the default script template, we'll put it back when done
        _script_template = zc.buildout.easy_install.script_template
        
        zc.buildout.easy_install.script_template = \
            zc.buildout.easy_install.script_header + template
        script = zc.buildout.easy_install.scripts(
                [(file_name, '', '')],
                ws,
                self.options['executable'],
                self.options['bin-directory'],
                extra_paths=extra_paths,
                arguments="")
        # put template back
        zc.buildout.easy_install.script_template = _script_template
        return script

wsgi_template = """

import os
import sys

sys.path[0:0] = [
    %(path)s,
]

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers import wsgi
application = wsgi.WSGIHandler()

"""

manage_template = """
import os
import sys

sys.path[0:0] = [
    %(path)s,
]

import manage

if __name__ == '__main__':
    manage.main()
"""
