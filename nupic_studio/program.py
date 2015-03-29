import os
import sys
import time
from PyQt4 import QtGui, QtCore
from nupic_studio.project import Project
from nupic_studio.ui import Global
from nupic_studio.ui.start_form import StartForm
from nupic_studio.ui.main_form import MainForm
from nupic_studio.ui.architecture_form import ArchitectureForm
from nupic_studio.ui.node_information_form import NodeInformationForm
from nupic_studio.ui.simulation_form import SimulationForm
from nupic_studio.ui.output_form import OutputForm

def main():
  Global.app = QtGui.QApplication(sys.argv)
  Global.app.setStyleSheet("QGroupBox { border: 1px solid gray; } QGroupBox::title { padding: 0 5px; }")

  Global.appPath = os.path.abspath(os.path.join(__file__, '..'))
  Global.loadConfig()

  Global.project = Project()
  Global.simulationForm = SimulationForm()
  Global.architectureForm = ArchitectureForm()
  Global.nodeInformationForm = NodeInformationForm()
  Global.outputForm = OutputForm()
  Global.mainForm = MainForm()

  # Create and display the splash screen
  start = time.time()
  splash_pix = QtGui.QPixmap(Global.appPath + '/images/splash.png')
  splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
  splash.setMask(splash_pix.mask())
  splash.show()
  while time.time() - start < 3:
    time.sleep(0.001)
    Global.app.processEvents()
  splash.close()

  # Show start form
  startForm = StartForm()
  startForm.show()

  deploymentBuild = os.getenv("NUPIC_STUDIO_DEPLOYMENT_BUILD", False)
  if deploymentBuild:
    sys.exit(0)
  else:
    sys.exit(Global.app.exec_())


if __name__ == '__main__':
  main()
