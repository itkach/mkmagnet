from distutils.core import setup

setup(name='mkmagnet',
      version='1.0',
      description='Generate magent link from torrent file',
      author='Igor Tkach',
      author_email='itkach@gmail.com',
      url='http://github.com/itkach/mkmagnet',
      license='Public Domain',
      py_modules = ['mkmagnet'],
      install_requires=['bencode'])
