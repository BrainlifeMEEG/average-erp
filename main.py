"""
Average epoched data into an evoked response.

This app loads epoched MNE data and averages either all epochs together
or a selected subset of stimulus conditions, producing an evoked
response, a joint plot, and a QC report.

Inputs:
    - fname: Path to epoched MNE data (.fif)
    - average-all: If true, average all epochs together
    - stimulus_names: Comma-separated stimulus conditions to average (used when average-all is false)
    - condition: Name of the condition being averaged (used when average-all is false)
    - peaks: Comma-separated peak times for plot_joint, or "None" for automatic

Outputs:
    - out_dir/ave.fif: Evoked data in MNE format
    - out_figs/evoked.png: Evoked joint plot
    - out_report/report.html: HTML report with the evoked response
    - product.json: Metadata about the averaging
"""

# Copyright (c) 2026 brainlife.io
#
# Author: Guiomar Niso

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    require_config_keys
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()
require_config_keys(config, ['epo', 'average-all', 'peaks'])

# == LOAD DATA ==
epo = mne.read_epochs(config['epo'])

# == AVERAGE ==
average_all = config['average-all']
if average_all is True or average_all == 'True':
    evo = epo.average()
    cond = 'All'
else:
    stimuli = config['stimulus_names'].split(',')
    evo = epo[stimuli].average()
    cond = config['condition']

peaks = config['peaks']
if peaks == 'None':
    peaks = 'auto'
else:
    peaks = [float(i) for i in peaks.split(',')]

# == CREATE FIGURE ==
fig = evo.plot_joint(times=peaks)
fig_path = os.path.join('out_figs', 'evoked.png')
fig.savefig(fig_path)

# == CREATE REPORT ==
report = mne.Report(title='Evoked Averaging Report')
report.add_evokeds(evo, titles=f'Evoked response for condition {cond}')
report.add_figure(fig, title=f'Evoked response for condition {cond}')
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == SAVE FILE ==
evo.save(os.path.join('out_dir', 'ave.fif'), overwrite=True)

# == CREATE PRODUCT.JSON ==
product_items = []
add_info_to_product(product_items, f'Averaged evoked response for condition "{cond}"', 'success')
add_image_to_product(product_items, 'Evoked response', filepath=fig_path)
create_product_json(product_items)
