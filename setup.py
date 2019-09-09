from __future__ import (
    absolute_import,
    unicode_literals,
)

from setuptools import (
    find_packages,
    setup,
)

from conformity import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


currency_requires = [
    'currint',
]

country_requires = [
    'pycountry',
]

tests_require = [
    'freezegun',
    'mypy;python_version>"3.4"',
    'pytest',
    'pytest-cov',
    'pytest-runner',
    'pytz',
] + currency_requires + country_requires

setup(
    name='conformity',
    version=__version__,
    author='Eventbrite, Inc.',
    author_email='opensource@eventbrite.com',
    description='Cacheable schema description and validation',
    long_description=readme(),
    url='http://github.com/eventbrite/conformity',
    packages=list(map(str, find_packages(include=['conformity', 'conformity.*']))),
    package_data={str('conformity'): [str('py.typed')]},  # PEP 561
    zip_safe=False,  # PEP 561
    include_package_data=True,
    install_requires=[
        'attrs>=17.4,<20',
        'six',
        'typing;python_version<"3.5"',
    ],
    tests_require=tests_require,
    setup_requires=['pytest-runner'],
    test_suite='tests',
    extras_require={
        'currency': currency_requires,
        'country': country_requires,
        'testing': tests_require,
    },
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
)
