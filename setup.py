"""
Flask-Mustache
-------------

`Mustache`__ integration for Flask.

Mustache::
"""
from setuptools import setup


setup(
    name='Flask-Mustache',
    version='0.1',
    url='https://github.com/bradleywright/flask-mustache',
    license='BSD',
    author='Bradley Wright',
    author_email='brad@intranation.com',
    description='Mustache integration for Flask.',
    long_description=__doc__,
    packages=['flask_mustache'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'pystache'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
