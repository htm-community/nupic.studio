import os
import sys
import time
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import REPO_DIR


def main():
    # Initialize Qt environment
    app = QtWidgets.QApplication(sys.argv)

    from nupic_studio.ui import Global
    from nupic_studio.project import Project
    Global.project = Project()

    # Start the Qt environment
    from nupic_studio.ui.main_window import MainWindow
    main_window = MainWindow()

    # Create and display the splash screen
    start = time.time()
    splash_pix = QtGui.QPixmap(os.path.join(REPO_DIR, 'images', 'splash.png'))
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    while time.time() - start < 3:
        time.sleep(0.001)
        app.processEvents()
    splash.close()

    # Show start form
    from nupic_studio.ui.start_window import StartWindow
    start_window = StartWindow(main_window)
    start_window.show()

    deployment_build = os.getenv("NUPIC_STUDIO_DEPLOYMENT_BUILD", False)
    if deployment_build:
        sys.exit(0)
    else:
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
