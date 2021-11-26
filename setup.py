from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Configurator',
    url='https://github.com/slavayssiere-spoon/configurator',
    author='Sebastien Lavayssiere',
    author_email='sebastien.lavayssiere@spoon.ai',
    # Needed to actually package something
    packages=['configurator'],
    # Needed for dependencies
    install_requires=[''],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='For SPooN Cloud configurator',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)