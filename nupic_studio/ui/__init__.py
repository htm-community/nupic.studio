import os
import copy
from PyQt5 import QtGui, QtCore, QtWidgets


class State:
    NO_STARTED = 0
    SIMULATING = 1
    PLAYBACKING = 2
    STOPPED = 3


DEFAULT_CONFIGURATION = {'views': [
    {'name': "Default", 'show_bits_none': False, 'show_bits_active': True, 'show_bits_predicted': True, 'show_bits_falsely_predicted': True, 'show_cells_none': False, 'show_cells_learning': True, 'show_cells_active': True, 'show_cells_predicted': True, 'show_cells_falsely_predicted': True, 'show_cells_inactive': False, 'show_proximal_segments_none': False, 'show_proximal_segments_active': True, 'show_proximal_segments_predicted': True, 'show_proximal_segments_falsely_predicted': True, 'show_proximal_synapses_none': False, 'show_proximal_synapses_connected': True, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': True, 'show_proximal_synapses_falsely_predicted': True, 'show_distal_segments_none': False, 'show_distal_segments_active': True, 'show_distal_synapses_none': False, 'show_distal_synapses_connected': True, 'show_distal_synapses_active': False},
    {'name': "Sensors Bits", 'show_bits_none': False, 'show_bits_active': True, 'show_bits_predicted': True, 'show_bits_falsely_predicted': True, 'show_cells_none': True, 'show_cells_learning': False, 'show_cells_active': False, 'show_cells_predicted': False, 'show_cells_falsely_predicted': False, 'show_cells_inactive': False, 'show_proximal_segments_none': True, 'show_proximal_segments_active': False, 'show_proximal_segments_predicted': False, 'show_proximal_segments_falsely_predicted': False, 'show_proximal_synapses_none': True, 'show_proximal_synapses_connected': False, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': False, 'show_proximal_synapses_falsely_predicted': False, 'show_distal_segments_none': True, 'show_distal_segments_active': False, 'show_distal_synapses_none': True, 'show_distal_synapses_connected': False, 'show_distal_synapses_active': False},
    {'name': "Spatial Activation", 'show_bits_none': False, 'show_bits_active': True, 'show_bits_predicted': False, 'show_bits_falsely_predicted': False, 'show_cells_none': False, 'show_cells_learning': False, 'show_cells_active': True, 'show_cells_predicted': False, 'show_cells_falsely_predicted': False, 'show_cells_inactive': False, 'show_proximal_segments_none': False, 'show_proximal_segments_active': True, 'show_proximal_segments_predicted': False, 'show_proximal_segments_falsely_predicted': False, 'show_proximal_synapses_none': False, 'show_proximal_synapses_connected': True, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': False, 'show_proximal_synapses_falsely_predicted': False, 'show_distal_segments_none': True, 'show_distal_segments_active': False, 'show_distal_synapses_none': True, 'show_distal_synapses_connected': False, 'show_distal_synapses_active': False},
    {'name': "Temporal Activation", 'show_bits_none': False, 'show_bits_active': False, 'show_bits_predicted': True, 'show_bits_falsely_predicted': True, 'show_cells_none': False, 'show_cells_learning': True, 'show_cells_active': False, 'show_cells_predicted': True, 'show_cells_falsely_predicted': True, 'show_cells_inactive': False, 'show_proximal_segments_none': False, 'show_proximal_segments_active': False, 'show_proximal_segments_predicted': True, 'show_proximal_segments_falsely_predicted': True, 'show_proximal_synapses_none': False, 'show_proximal_synapses_connected': False, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': True, 'show_proximal_synapses_falsely_predicted': True, 'show_distal_segments_none': False, 'show_distal_segments_active': True, 'show_distal_synapses_none': False, 'show_distal_synapses_connected': True, 'show_distal_synapses_active': False},
    {'name': "Active Elements", 'show_bits_none': False, 'show_bits_active': True, 'show_bits_predicted': False, 'show_bits_falsely_predicted': False, 'show_cells_none': False, 'show_cells_learning': True, 'show_cells_active': True, 'show_cells_predicted': False, 'show_cells_falsely_predicted': False, 'show_cells_inactive': False, 'show_proximal_segments_none': False, 'show_proximal_segments_active': True, 'show_proximal_segments_predicted': False, 'show_proximal_segments_falsely_predicted': False, 'show_proximal_synapses_none': False, 'show_proximal_synapses_connected': True, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': False, 'show_proximal_synapses_falsely_predicted': False, 'show_distal_segments_none': False, 'show_distal_segments_active': True, 'show_distal_synapses_none': False, 'show_distal_synapses_connected': True, 'show_distal_synapses_active': False},
    {'name': "Predicted Elements", 'show_bits_none': False, 'show_bits_active': False, 'show_bits_predicted': True, 'show_bits_falsely_predicted': True, 'show_cells_none': False, 'show_cells_learning': False, 'show_cells_active': False, 'show_cells_predicted': True, 'show_cells_falsely_predicted': True, 'show_cells_inactive': False, 'show_proximal_segments_none': False, 'show_proximal_segments_active': False, 'show_proximal_segments_predicted': True, 'show_proximal_segments_falsely_predicted': True, 'show_proximal_synapses_none': False, 'show_proximal_synapses_connected': False, 'show_proximal_synapses_active': False, 'show_proximal_synapses_predicted': True, 'show_proximal_synapses_falsely_predicted': True, 'show_distal_segments_none': True, 'show_distal_segments_active': False, 'show_distal_synapses_none': True, 'show_distal_synapses_connected': False, 'show_distal_synapses_active': False},
]}


NEW_VIEW = {
    'menu': None,
    'name': "",
    'show_bits_none': False,
    'show_bits_active': True,
    'show_bits_predicted': True,
    'show_bits_falsely_predicted': True,
    'show_cells_none': False,
    'show_cells_learning': True,
    'show_cells_active': True,
    'show_cells_predicted': True,
    'show_cells_falsely_predicted': True,
    'show_cells_inactive': True,
    'show_proximal_segments_none': False,
    'show_proximal_segments_active': True,
    'show_proximal_segments_predicted': True,
    'show_proximal_segments_falsely_predicted': True,
    'show_proximal_synapses_none': False,
    'show_proximal_synapses_connected': True,
    'show_proximal_synapses_active': True,
    'show_proximal_synapses_predicted': True,
    'show_proximal_synapses_falsely_predicted': True,
    'show_distal_segments_none': False,
    'show_distal_segments_active': True,
    'show_distal_synapses_none': False,
    'show_distal_synapses_connected': True,
    'show_distal_synapses_active': True,
}


class Global:
    app_path = ''
    version = '0.1.0'

    simulation_initialized = False
    curr_step = 0
    sel_step = 0
    time_steps_predictions_chart = None
    output = []

    views = []

    project = None
    architecture_form = None
    node_information_form = None
    simulation_form = None
    output_form = None
    main_form = None

    @staticmethod
    def loadConfig():
        """
        Loads the content from XML file to config the program.
        """
        file_name = os.path.join(Global.app_path, "nupic_studio.config")
        try:
            config = eval(open(file_name, 'r').read())
        except:
            QtWidgets.QMessageBox.warning(None, "Warning", "Cannot read the config file (" + file_name + ")! Configuration was reseted!", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Default, QtWidgets.QMessageBox.NoButton)
            config = DEFAULT_CONFIGURATION
        Global.views = config['views']

    @staticmethod
    def saveConfig():
        """
        Saves the content from current program's configuration.
        """
        file_name = os.path.join(Global.app_path, "nupic_studio.config")
        views = copy.deepcopy(Global.views)
        for view in views:
            view['menu'] = None
        config = {'views': views}
        open(file_name, 'w').write(str(config))
