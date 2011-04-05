from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

setup(
    name = 'django-agenda',
    version = "0.1",
    description = 'An event agenda application for Django 1.0+.',
    long_description = README,
    author = 'Mathijs de Bruin',
    author_email = 'mathijs@mathijsfietst.nl',
    url = 'http://github.com/dokterbob/django-agenda',
    packages = find_packages(),
    include_package_data = True,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
