import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.8.2'
PACKAGE_NAME = 'ra_pickles'
AUTHOR = 'Shah Rukh Qasim'
AUTHOR_EMAIL = 'shah.rukh.qasim@cern.ch'
URL = 'https://github.com/shahrukhqasim/ra_pickles'

LICENSE = 'MIT License'
DESCRIPTION = 'A simple package that allows creating a pickles dataset and fast random access'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )