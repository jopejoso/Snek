from setuptools import setup

setup(
   name='snekpy',
   version='0.2',
   description='Simple ASCII snake game',
   author='Josip Kasap',
   author_email='jjopek0@gmail.com',
   packages=['snekpy'],  #Same as name
   install_requires=['pynput'], #external packages as dependencies
)
