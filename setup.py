from setuptools import setup, find_packages

REQUIREMENTS = (
    'django>=1.11,<3',
)
TEST_REQUIREMENTS = (
    'mock',
    'django-debug-toolbar',
)

from contact_form import VERSION

setup(
    name="django-contact-form-gv",
    version=VERSION,
    author="Aaron Madison",
    description="Django Contact Form using class based views.",
    long_description=open('README.rst', 'r').read(),
    url="https://github.com/madisona/django-contact-form",
    packages=find_packages(exclude=["example*"]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='runtests.runtests',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
