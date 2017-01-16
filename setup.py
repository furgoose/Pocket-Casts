from setuptools import setup
import pocketcasts

def read_file(name):
    with open(name) as fd:
        return fd.read()

setup(
    name="pocketcasts-api",
    version=pocketcasts.__version__,
    author=pocketcasts.__author__,
    description=pocketcasts.__doc__,
    url=pocketcasts.__url__,
    license='MIT',
    py_modules=['pocketcasts'],
    long_description=read_file('README.md')
)