"""
----------------
  Flask-Mustache
----------------

`Mustache`__ integration for Flask.

__ http://mustache.github.com/

Flask-Mustache adds template helpers and context processors to assist
Flask developers with integrating the Mustache library into their
development process.

"""
from setuptools import setup


setup(
    name='Flask-MustacheJS',
    version='0.4.8',
    url='https://github.com/bradleywright/flask-mustachejs',
    license='BSD',
    author='Bradley Wright',
    author_email='brad@intranation.com',
    description='Mustache integration in Flask, with Jinja and client-side libraries.',
    long_description=__doc__,
    packages=['flask_mustache'],
    zip_safe=False,
    include_package_data=True,
    # include static assets
    package_data = {
        '': ['*.jinja', '*.js']
    },
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
