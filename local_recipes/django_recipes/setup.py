
from setuptools import setup

VERSION = 0.1

setup(name="django_recipes",
      version=VERSION,
      entry_points = """
      [zc.buildout]
      default = script:Recipe
      """
      )
