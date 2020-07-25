import os
import sys
import time
from PyQt5 import QtGui, QtCore, QtWidgets, QtOpenGL
from nupic_studio.project import Project
from nupic_studio.ui import Global
from nupic_studio.ui.start_window import StartWindow
from nupic_studio.ui.main_window import MainWindow
from nupic_studio.ui.architecture_window import ArchitectureWindow
from nupic_studio.ui.node_information_window import NodeInformationWindow
from nupic_studio.ui.simulation_window import SimulationWindow
from nupic_studio.ui.output_window import OutputWindow


def main():
    Global.app = QtWidgets.QApplication(sys.argv)
    Global.app.setStyleSheet("QGroupBox { border: 1px solid gray; } QGroupBox::title { padding: 0 5px; }")

    Global.app_path = os.path.abspath(os.path.join(__file__, '..'))
    Global.loadConfig()

    Global.project = Project()
    Global.simulation_window = SimulationWindow()
    Global.architecture_window = ArchitectureWindow()
    Global.node_information_window = NodeInformationWindow()
    Global.output_window = OutputWindow()
    Global.main_window = MainWindow()

    # Create and display the splash screen
    start = time.time()
    splash_pix = QtGui.QPixmap(Global.app_path + '/images/splash.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    while time.time() - start < 3:
        time.sleep(0.001)
        Global.app.processEvents()
    splash.close()

    # Show start form
    start_window = StartWindow()
    start_window.show()

    deployment_build = os.getenv("NUPIC_STUDIO_DEPLOYMENT_BUILD", False)
    if deployment_build:
        sys.exit(0)
    else:
        sys.exit(Global.app.exec_())


if __name__ == '__main__':
    main()
