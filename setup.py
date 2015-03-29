import sys
import os
import subprocess
import tempfile
import shutil
import urllib2
import tarfile
import zipfile
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


def downloadFile(url, destFile, silent=False):
  """
  Download a file to the specified location
  """

  if not silent:
    print "Downloading from\n\t%s\nto\t%s.\n" % (url, destFile)

  destDir = os.path.dirname(destFile)
  if not os.path.exists(destDir):
    os.makedirs(destDir)

  try:
    response = urllib2.urlopen(url)
  except urllib2.URLError:
    return False

  with open(destFile, "wb") as fileObj:
    totalSize = response.info().getheader("Content-Length").strip()
    totalSize = int(totalSize)
    bytesSoFar = 0

    # Download chunks writing them to target file
    chunkSize = 8192
    oldPercent = 0
    while True:
      chunk = response.read(chunkSize)
      bytesSoFar += len(chunk)

      if not chunk:
        break

      fileObj.write(chunk)

      # Show progress
      if not silent:
        percent = (float(bytesSoFar) / totalSize) * 100
        percent = int(percent)
        if percent != oldPercent and percent % 5 == 0:
          print ("Downloaded %i of %i bytes (%i%%)."
                 % (bytesSoFar, totalSize, int(percent)))
          oldPercent = percent

  return True


def unpackFile(package, dirToUnpack, destDir, silent=False):
  """
  Unpack package file to the specified directory
  """

  if not silent:
    print "Unpacking %s into %s..." % (package, destDir)

  if package.endswith(".zip"):
    file = zipfile.ZipFile(package)
  else:
    file = tarfile.open(package, "r")
  file.extractall(destDir)

  # Copy subdirectories to a level up
  subDirs = os.listdir(destDir + "/" + dirToUnpack)
  for subDir in subDirs:
    shutil.rmtree(destDir + "/" + subDir, True)
    shutil.move(destDir + "/" + dirToUnpack + "/" + subDir,
                destDir + "/" + subDir)
  
  shutil.rmtree(destDir + "/" + dirToUnpack, True)


def installPackageFromSource(name, urlRepo, pkgBaseName, pkgExtension, configScript, silent=False):
  """
  Install manually packages from source that cannot be installed via pip
  """

  tempDir = tempfile.gettempdir()
  srcFile = urlRepo + "/" + pkgBaseName + pkgExtension
  dstFile = tempDir + "/" + pkgBaseName + pkgExtension

  print "Downloading %s package..." % name
  downloadSuccess = downloadFile(srcFile, dstFile, silent)
  
  if not downloadSuccess:
    raise Exception("Failed to download %s package from %s!"
                    "Ensure you have an internet connection and that "
                    "the remote package exists." % (name, srcFile))
  else:
    print "Download successful."
    
    # Unpack package to a temp dir
    unpackFile(dstFile,
               pkgBaseName,
               tempDir + "/" + pkgBaseName,
               silent)

    # Build and install package
    print "Installing %s..." % name
    os.chdir(tempDir + "/" + pkgBaseName)

    proc = subprocess.Popen("python " + configScript, shell=True)
    _, err = proc.communicate()
    if err:
      print err
      raise Exception("Failed to configure %s! Try install manually this python package." % name)
    
    proc = subprocess.Popen("make -j 4", shell=True)
    _, err = proc.communicate()
    if err:
      raise Exception("Failed to build %s! Try install manually this python package." % name)
    
    proc = subprocess.Popen("make install", shell=True)
    _, err = proc.communicate()
    if err:
      raise Exception("Failed to install %s! Try install manually this python package." % name)


def installPackageFromBinaries(name, urlFile, silent=False):
  """
  Install manually packages from binaries that cannot be installed via pip
  """

  tempDir = tempfile.gettempdir()
  srcFile = urlFile
  dstFile = tempDir + "/" + os.path.basename(urlFile)

  print "Downloading %s package..." % name
  downloadSuccess = downloadFile(srcFile, dstFile, silent)
  
  if not downloadSuccess:
    raise Exception("Failed to download %s package from %s!"
                    "Ensure you have an internet connection and that "
                    "the remote package exists." % (name, srcFile))
  else:
    print "Download successful."

    # Install package
    print "Installing %s..." % name
    os.chdir(tempDir)

    proc = subprocess.Popen(dstFile + " /S")
    _, err = proc.communicate()
    if err:
      raise Exception("Failed to install %s! Try install manually this python package." % name)


def checkPyQtInstalled():
  """
  Install PyQt in case of not found
  """
  
  import imp
  try:
    imp.find_module("PyQt4")
    moduleFound = True
  except ImportError:
    moduleFound = False
  
  if not moduleFound:
    if platform == "windows":
      pkgExtension = ".zip"
      installFromSource = False
    else:
      pkgExtension = ".tar.gz"
      installFromSource = True
  
    if installFromSource:
      installPackageFromSource(
        "SIP4",
        "http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.6",
        "sip-4.16.6",
        pkgExtension,
        "configure.py")
    
      pkgBaseName = ""
      if platform == "linux":
        pkgBaseName = "PyQt-x11-gpl-4.11.3"
      elif platform == "darwin":
        pkgBaseName = "PyQt-mac-gpl-4.11.3"
      elif platform == "windows":
        pkgBaseName = "PyQt-win-gpl-4.11.3"
      installPackageFromSource(
        "PyQt4",
        "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3",
        pkgBaseName,
        pkgExtension,
        "configure.py --confirm-license")
    else:
      installPackageFromBinaries(
        "PyQt4",
        "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe")


def checkNuPICInstalled():
  """
  Install NuPIC in case of not found
  """
  
  import imp
  try:
    imp.find_module("nupic")
    moduleFound = True
  except ImportError:
    moduleFound = False
  
  if not moduleFound:
    raise Exception("NuPIC library not found! Access https://github.com/numenta/nupic/ for get help on how install it.")


platform, bitness = getPlatformInfo()

checkNuPICInstalled()
checkPyQtInstalled()

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
