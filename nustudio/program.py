import os
import sys
import time
from PyQt4 import QtGui, QtCore
from nustudio.project import Project
from nustudio.ui import Global
from nustudio.ui.start_form import StartForm
from nustudio.ui.main_form import MainForm
from nustudio.ui.node_selector_form import NodeSelectorForm
from nustudio.ui.node_information_form import NodeInformationForm
from nustudio.ui.simulation_form import SimulationForm
from nustudio.ui.output_form import OutputForm

def main():
	app = QtGui.QApplication(sys.argv)
	app.setStyleSheet("QGroupBox { border: 1px solid gray; } QGroupBox::title { padding: 0 5px; }")

	Global.appPath = os.path.abspath(os.path.join(__file__, '..'))
	Global.loadConfig()

	Global.project = Project()
	Global.simulationForm = SimulationForm()
	Global.nodeSelectorForm = NodeSelectorForm()
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
		app.processEvents()
	splash.close()

	# Show start form
	startForm = StartForm()
	startForm.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()