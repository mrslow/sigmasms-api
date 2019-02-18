from setuptools import setup

with open('README.md') as f:
    readme = f.read()

dependencies = ['reuqests']

setup(
    name='sigmasms',
    version='0.1',
    description='Tool for easy working with sigmasms API',
    long_description=readme,
    author='Anton Shchetikhin',
    author_email='animal2k@gmail.com',
    py_modules=['sigmasms'],
    url='https://github.com/mrslow/sigmasms',
    keywords=['api', 'sms', 'sigmasms']
)
