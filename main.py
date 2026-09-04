"""
Average epoched data into one or more evoked responses.

This app loads epoched MNE data and averages either all epochs together, or
one or more named groups of stimulus conditions, producing one evoked
response per group (all saved together in a single Evoked file), a joint
plot per group, and a QC report.

Inputs:
    - epo: Path to epoched MNE data (.fif)
    - average_all: If true, average all epochs together into one Evoked
      (ignores stimulus_names/condition)
    - stimulus_names: One or more groups of comma-separated stimulus
      conditions to average, separated by semicolons if there's more than
      one group (used when average_all is false). Conditions within a
      group are pooled into a single Evoked; each group produces its own
      Evoked. E.g. "face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar"
      produces two Evokeds. A value with no semicolon is a single group,
      identical to the app's previous single-condition behavior.
    - condition: Name(s) for each group, matching stimulus_names 1:1,
      semicolon-separated if there's more than one group (used when
      average_all is false)
    - peaks: Comma-separated peak times for plot_joint (applied to every
      group), or "None" for automatic

Outputs:
    - out_dir/ave.fif: One or more Evoked responses in MNE format (one per
      condition group)
    - out_figs/evoked*.png: Evoked joint plot(s), one set per condition
    - out_report/report.html: HTML report with the evoked response(s)
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
    save_figure_with_base64,
    require_config_keys
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()
require_config_keys(config, ['epo', 'average_all', 'peaks'])

# == LOAD DATA ==
epo = mne.read_epochs(config['epo'])

# == AVERAGE ==
# evo_list always holds one or more mne.Evoked, one per condition group.
# average_all=True is just the len(evo_list) == 1 case with a fixed label.
average_all = config['average_all']
if average_all is True or average_all == 'True':
    evo = epo.average()
    evo.comment = 'All'
    evo_list = [evo]
else:
    # ';' separates independent groups, each producing its own Evoked;
    # ',' within a group still means "pool these conditions together"
    # (unchanged meaning from before). A config with no ';' is exactly one
    # group -- identical to the previous single-condition behavior.
    stim_groups = config['stimulus_names'].split(';')
    cond_labels = config['condition'].split(';')
    if len(stim_groups) != len(cond_labels):
        product_items = []
        add_info_to_product(
            product_items,
            f"stimulus_names has {len(stim_groups)} group(s) but condition has "
            f"{len(cond_labels)} label(s) -- they must match 1:1 "
            f"(semicolon-separated, one label per group).",
            'error'
        )
        create_product_json(product_items)
        sys.exit(1)
    evo_list = []
    for group, label in zip(stim_groups, cond_labels):
        stimuli = [s.strip() for s in group.split(',')]
        ev = epo[stimuli].average()
        ev.comment = label.strip()
        evo_list.append(ev)

peaks = config['peaks']
if peaks == 'None':
    peaks = 'auto'
else:
    peaks = [float(i) for i in peaks.split(',')]

multi = len(evo_list) > 1

# == CREATE REPORT (figures added here, before any are closed below) ==
report = mne.Report(title='Evoked Averaging Report')
report.add_evokeds(
    evo_list if multi else evo_list[0],
    titles=[e.comment for e in evo_list] if multi else evo_list[0].comment,
)

# == CREATE FIGURES ==
# plot_joint() returns a single Figure only when the data has one channel
# type; with multiple types (mag+grad+eeg here) it returns a list, one
# figure per type -- normalize to a list either way, per condition.
# report.add_figure() is called here (while the figure is still fully
# live) *before* save_figure_with_base64 below, which closes it once
# saved -- reusing a closed Figure for report embedding isn't safe to
# assume, so the ordering here is deliberate, not incidental.
fig_base64 = {}
for evo in evo_list:
    fig = evo.plot_joint(times=peaks)
    report.add_figure(fig, title=f'Evoked response for condition {evo.comment}')
    figs = fig if isinstance(fig, list) else [fig]
    for i, f in enumerate(figs):
        if not multi and len(figs) == 1:
            fname, label = 'evoked.png', 'Evoked response'
        elif len(figs) == 1:
            fname, label = f'evoked_{evo.comment}.png', f'Evoked response: {evo.comment}'
        else:
            fname, label = f'evoked_{evo.comment}_{i}.png', f'Evoked response: {evo.comment} ({i})'
        fp = os.path.join('out_figs', fname)
        fig_base64[label] = save_figure_with_base64(f, fp, dpi_file=150, dpi_base64=80)

report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == SAVE FILE ==
# mne.write_evokeds (not Evoked.save(), which has no multi-evoked support)
# so this works whether evo_list has one condition or several.
mne.write_evokeds(os.path.join('out_dir', 'ave.fif'), evo_list, overwrite=True)

# == CREATE PRODUCT.JSON ==
product_items = []
labels = ', '.join(f'"{e.comment}"' for e in evo_list)
add_info_to_product(
    product_items,
    f'Averaged {len(evo_list)} evoked response(s): {labels}',
    'success'
)
# Low-dpi thumbnails, not a raw re-read of the full-res out_figs/ files --
# several conditions' figures embedded at full resolution risks the same
# 1MB product.json cap noise-covariance hit (see that app's own fix).
for name, b64 in fig_base64.items():
    add_image_to_product(product_items, name, base64_data=b64)
create_product_json(product_items)
