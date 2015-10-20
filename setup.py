from setuptools import setup

setup(
    name='validator.py',
    version='1.2.2',
    author='Samuel "mansam" Lucidi',
    author_email="mansam@csh.rit.edu",
    packages=['validator'],
    url='https://github.com/mansam/validator.py',
    license='MIT',
    description='A library for validating that dictionary values meet certain sets of parameters. Much like form validators, but for dicts.',
    long_description=open('README.rst').read()
)
