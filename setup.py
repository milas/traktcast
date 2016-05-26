from setuptools import setup

setup(
    name='traktcast',
    version='0.6',
    packages=['traktcast'],
    url='https://www.github.com/milas/traktcast',
    license='MIT',
    author='Milas Bowman',
    author_email='milas.bowman@gmail.com',
    description='Automatically scrobble what\'s playing from Chromecast to Trakt',
    install_requires=[
        'pychromecast',
        'trakt.py',
        'requests>=2.0'
    ],
    setup_requires=[
        'flake8'
    ]
)
