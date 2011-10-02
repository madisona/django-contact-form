
from setuptools import setup, find_packages

REQUIREMENTS = (
    'django>=1.3',
)
TEST_REQUIREMENTS = (
    'south',
    'mock',
    'django-debug-toolbar',
)

from contact_form import VERSION

setup(
    name="django-contact-form-gv",
    version=VERSION,
    author="Aaron Madison",
    description="Django Contact Form using class based views.",
    long_description=open('README', 'r').read(),
    url="https://github.com/madisona/django-contact-form",
    packages=find_packages(exclude=["example"]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='runtests.runtests',
    zip_safe=False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)