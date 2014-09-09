import sys
import os
import subprocess
from setuptools import setup, find_packages

"""
This file should called to install the NuPIC Studio.
"""

repositoryDir = os.getcwd()


# Check if no option was passed, i.e. if "setup.py" is the only option
# If True, "develop" is passed by default
# This is useful when a developer wish build the project directly from an IDE
if len(sys.argv) == 1:
	print "No command passed. Using 'develop' as default command. Use python setup.py --help' for more information."
	sys.argv.append("develop")


# Get properties of the project like version, notes, etc
properties = {}
execfile(os.path.join(repositoryDir, "nustudio", "__init__.py"), {}, properties)


# Call the setup process
os.chdir(repositoryDir)
setup(
	name = 'nustudio',
	version = properties["__version__"],
	packages = find_packages(),
	package_data = {
		'': ['README.md', 'LICENSE'],
		'nustudio': ['nustudio.config'],
		'nustudio.images': ['*'],
		'nustudio.projects': ['*']},
	entry_points = {
		'gui_scripts': ['nustudio = nustudio.program:main']},
	description = 'NuPIC Studio is a virtual studio that allows developers to create, debug, and visualize HTM networks from NuPIC library',
	author='David Ragazzi',
	author_email='david_ragazzi@hotmail.com',
	url='https://github.com/numenta/nupic.studio',
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
		"PyOpenGL",
		"PyOpenGL-accelerate",
		"PyQtGraph"],
	long_description = """NuPIC Studio is a virtual studio that allows developers to create, debug, and visualize HTM networks from NuPIC library. Some of its advantages:
* Users can open, save, or change their "HTM projects" or of other developers. A typical project contains data to be trained, neural network configuration, statistics, etc, which can be shared to be analysed or integrated with other projects.
* Users can create their own encoders and sensors to feed the HTM network.
* Any changes in the nupic source can be immediatedly viewed. This helps users that wish test improvements like hierarchy, attention, and motor integration.
For more information, see numenta.org or the NuPIC wiki (https://github.com/numenta/nupic.studio/wiki)."""
)
