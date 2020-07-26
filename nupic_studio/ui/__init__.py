import os
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import REPO_DIR

ICON = QtGui.QIcon(os.path.join(REPO_DIR, 'images', 'logo.ico'))


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
    curr_step = 0
    sel_step = 0
    time_steps_predictions_chart = None
    project = None
