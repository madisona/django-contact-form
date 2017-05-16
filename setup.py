from setuptools import setup, find_packages

REQUIREMENTS = (
    'django>=1.8',
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
        "Framework :: Django :: 1.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
