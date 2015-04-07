import sys
import os
from setuptools import setup, find_packages

"""
This file should called to install the NuPIC Studio.
"""

REPO_DIR = os.getcwd()


def getPlatformInfo():
  """
  Identify platform
  """
  if "linux" in sys.platform:
    platform = "linux"
  elif "darwin" in sys.platform:
    platform = "darwin"
  elif "win32" in sys.platform:
    platform = "windows"
  else:
    raise Exception("Platform '%s' is unsupported!" % sys.platform)

  if sys.maxsize > 2**32:
    bitness = "64"
  else:
    bitness = "32"

  return platform, bitness


platform, bitness = getPlatformInfo()

# Get properties of the project like version, notes, etc
properties = {}
execfile(os.path.join(REPO_DIR, "nupic_studio", "__init__.py"), {}, properties)

# Call the setup process
os.chdir(REPO_DIR)
setup(
  name = 'nupic_studio',
  version = properties["__version__"],
  packages = find_packages(),
  package_data = {
    '': ['README.md', 'LICENSE'],
    'nupic_studio': ['nupic_studio.config'],
    'nupic_studio.images': ['*'],
    'nupic_studio.projects': ['*']},
  entry_points = {
    'gui_scripts': ['nupic_studio = nupic_studio.program:main']},
  description = 'NuPIC Studio is a virtual studio that allows developers to create, debug, and visualize HTM networks from NuPIC library',
  author='David Ragazzi',
  author_email='david_ragazzi@hotmail.com',
  url='https://github.com/nupic-community/nupic.studio',
  classifiers=[
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence'
  ],
  install_requires = [
    "PyOpenGL==3.1.0",
    "pyqtgraph==0.9.10"],
  long_description = """NuPIC Studio is a virtual studio that allows developers to create, debug, and visualize HTM networks from NuPIC library. Some of its advantages:
* Users can open, save, or change their "HTM projects" or of other developers. A typical project contains data to be trained, neural network configuration, statistics, etc, which can be shared to be analysed or integrated with other projects.
* Users can create their own encoders and sensors to feed the HTM network.
* Any changes in the nupic source can be immediatedly viewed. This helps users that wish test improvements like hierarchy, attention, and motor integration.
For more information, see numenta.org or the NuPIC wiki (https://github.com/nupic-community/nupic.studio/wiki)."""
)
