from setuptools import setup, find_packages

setup(
    name='traktcast',
    version='0.6',
    packages=find_packages(),
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
