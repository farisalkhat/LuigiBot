from distutils.core import setup

setup(
    name='LuigiBot',
    version='0.1.0',
    author='Faris "Lefty" Al-khatahtbeh',
    author_email='farisalkhat@gmail.com',
    packages=['cogs'],
    url='https://github.com/farisalkhat/LuigiBot',
    license='LICENSE.txt',
    description='A general-purpose Discord bot.',
    long_description=open('README.txt').read(),
    install_requires=[
        "discord.py == 1.2.0",
    ],
)