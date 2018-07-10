import pocketcasts
from setuptools import setup, find_packages

setup(
    name="pocketcasts-api",

    version=pocketcasts.api.__version__,

    description=pocketcasts.api.__doc__,

    url=pocketcasts.api.__url__,

    author=pocketcasts.api.__author__,
    author_email='ferguslongley@live.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['testing']),

    keywords='podcasts pocketcasts',

    install_requires=['requests'],

    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
