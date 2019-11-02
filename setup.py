from setuptools import setup

setup(
    name='LuigiBot',
    version='0.1.0',
    author='Faris "Lefty" Al-khatahtbeh',
    author_email='farisalkhat@gmail.com',
    packages=[''],
    url='https://github.com/farisalkhat/LuigiBot',
    license='LICENSE.txt',
    description='A general-purpose Discord bot.',
    long_description=open('README.txt').read(),
    install_requires=[
        "discord.py == 1.2.0",
        "praw==6.3.1",
        "async_timeout==3.0.1",
        "pyosu==0.5.2",
        "random_cat==1.0.1",
        "requests==2.22.0",
        "geopy==1.20.0",
        "youtube_dl==2019.6.8",
        "SQLAlchemy==1.3.5",
        "Pillow==6.2.0",
        "tzwhere==3.0.3",
    ],
)
