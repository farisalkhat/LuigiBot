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
        "praw==6.3.1",
        "async_timeout==3.0.1",
        "pyosu==0.5.2",
        "random_cat==1.0.1",
        "requests==2.22.0",
        "geopy==1.20.0",
        "youtube_dl==2019.6.8",
        "SQLAlchemy==1.3.5",
        "youtube_data_api==0.0.16",
        "Pillow==6.1.0",
        "cat==0.0.1",
        "discord==1.0.1",
        "tzwhere==3.0.3",
        "youtube_api==0.1"
    ],
)