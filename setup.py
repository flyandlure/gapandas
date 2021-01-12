from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gapandas',
    packages=['gapandas'],
    version='0.18',
    license='MIT',
    description='GAPandas is a Python package for accessing Google Analytics API data using Pandas for use in models, '
                'reports or visualisations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Clarke',
    author_email='matt@flyandlure.org',
    url='https://github.com/flyandlure/gapandas',
    download_url='https://github.com/flyandlure/gapandas/archive/master.zip',
    keywords=['python', 'google analytics', 'ga', 'pandas', 'universal analytics'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pandas', 'google-api-python-client', 'oauth2client']
)
