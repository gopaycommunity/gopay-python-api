from setuptools import setup
from pypandoc import convert

setup(
    name='gopay',
    version='1.0.0rc1',
    description='GoPay\'s Python SDK for Payments REST API',
    long_description=convert('README.md', 'rst'),
    url='https://github.com/gopaycommunity/gopay-python-sdk',
    author='GoPay',
    author_email='integrace@gopay.cz',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='gopay payments sdk rest api',
    packages=['gopay'],
    install_requires=['requests'],
)