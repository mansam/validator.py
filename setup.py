from setuptools import setup

setup(
    name='validator.py',
    version='1.2.5',
    author='Samuel "mansam" Lucidi',
    author_email="sam@samlucidi.com",
    packages=['validator'],
    url='https://github.com/mansam/validator.py',
    description='A library for validating that dictionary values meet certain sets of parameters. Much like form validators, but for dicts.',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    license='MIT'
)
