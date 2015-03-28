## ![NuStudio Logo](https://github.com/nupic-community/nupic.studio/blob/master/nustudio/images/logo.png) NuPIC Studio ![*nix Build Status](https://travis-ci.org/nupic-community/nupic.studio.svg?branch=master)

NuPIC Studio is an all­-in-­one tool that allows users create a HTM neural network from scratch, train it, collect statistics, and share it among the members of the community. It is not just a visualization tool but an HTM builder, debugger and laboratory for experiments. It is ideal for newbies with little intimacy with NuPIC code as well as experts that wish a better productivity. Among its features and advantages:
 * Users can open, save, or change their "HTM projects" or of other developers. A typical project contains data to be trained, neural network configuration, statistics, etc, which can be shared to be analysed or integrated with other projects.
 * The HTM engine is the own original NuPIC libray (Python distribution). This means no port, no bindings, no re-implementation, etc. So any changes in the original nupic source can be immediatedly viewed. This helps users that wish test improvements like new encoders or even hierarchy, attention, and motor integration.

![Screenshot](https://github.com/nupic-community/nupic.studio/blob/master/doc/main_form.png)
 

For more information, see [numenta.org](http://numenta.org) or the [NuPIC Studio wiki](https://github.com/nupic-community/nupic.studio/wiki).

## Installation

Currently supported platforms:

 * Linux (32/64bit)
 * Mac OSX

Dependencies:

 * Python (2.7 or later) (with development headers)
 * PIP
 * NuPIC
 * NumPy
 * PyOpenGL
 * PyOpenGL-accelerate
 * PyQt4
 * PyQtGraph

_Note_: Except Python, PIP and NuPIC, all dependencies above are already automatically installed by PIP package. However some packages like PyQt4 might present errors due to conflicts specific to each system environment. In this case, you will have to install these packages manually using a package manager like apt, yum, or brew:

    apt-get install python-qt4 python-qt4-gl
    yum install PyQt4
    brew install pyqt

## User instructions

If you want only use it, simply do this:

    pip install nustudio

_Note_: If you get a "permission denied" error when using pip, you may add the --user flag to install to a location in your home directory, which should resolve any permissions issues. Doing this, you may need to add this location to your PATH and PYTHONPATH. Alternatively, you can run pip with 'sudo'.

Once it is installed, you can execute the app using:

    nustudio

and then click on `Open Project` button to open any example to getting started with NuPIC.

## Developer instructions

If you want develop, debug, or simply test NuPIC Studio, clone it and follow the instructions:

### Using command line

> This assumes the `NUPIC_STUDIO` environment variable is set to the directory where the NuPIC Studio source code exists.

    cd $NUPIC_STUDIO
    python setup.py build
    python setup.py develop

### Using an IDE

The following instructions will work in the most Python IDEs:

 * Open your IDE.
 * Open a project specifying the `$NUPIC_STUDIO` repository folder as location.
 * Click with mouse right button on `setup.py` file listed on project files and select `Run` command on pop-up menu. This will call the build process. Check `output` panel to see the result.
 * If the build was successful, just click on `program.py` and voilà!

If you don't have a favourite Python IDE, this article can help you to choose one: http://pedrokroger.net/choosing-best-python-ide/
