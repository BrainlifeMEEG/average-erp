# Average ERPs

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Brainlife.io app: average MEG/EEG epochs into one or more condition ERPs (Evoked)**

Uses Epochs.average() either on all epochs or on named groups of conditions (';'-separated) to produce one or more Evoked objects, saved together in ave.fif, with a joint plot per group and an HTML report. Use it after epoching to get ERPs/ERFs per condition.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meeg/mne/epochs` |
| 📤 **Outputs** | `neuro/meeg/mne/evoked` · `generic/image/png` · `report/html` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 1 CPUs · 8 GB memory |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.949](https://doi.org/10.25663/brainlife.app.949) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `evoked` | `neuro/meeg/mne/epochs` | yes | Epoched MEG/EEG data (MNE -epo.fif). |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/evoked` | One or more Evoked objects (ave.fif). |
| `out_figs` | `generic/image/png` | Joint ERP plots per condition group. |
| `out_dir_report` | `report/html` | HTML report with evoked traces and joint plots. |

<details>
<summary><b>⚙️ Parameters</b> (4)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `average_all` | boolean | `false` | Do you want all of your epoch types/stimuli/conditions to be averaged together? If not, enter the names of the epoch types/stimuli/conditions in the string below. |
| `stimulus_names` | string |  | Stimulus/condition names to average. To produce SEVERAL Evokeds in one run, separate independent groups with ";"; within a group, conditions are still pooled together with "," (e.g. "face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar" produces two Evokeds). A value with no ";" is a single group -- one Evoked, same as before. |
| `condition` | string |  | Name(s) for each group in stimulus_names, matching 1:1 and ";"-separated the same way (e.g. "face;scrambled" for the example above). Used as each output Evoked's label. Just enter the name(s) with no quotation marks. |
| `peaks` | string | `None` | Add a list (comma-separated) of time values at which you would like to display topomaps on a joint ERP plot. |

</details>

📚 **References used by this App:**
- Hayashi S, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21:809-813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.949-blue.svg)](https://doi.org/10.25663/brainlife.app.949)

## Description

This Brainlife.io app creates one or more Evoked (ERP/ERF) objects from epoched MEG/EEG data,
using MNE-Python's `Epochs.average()`. It can average all epochs into a single Evoked, or average
one or more named groups of stimulus conditions (selected with `Epochs[stimuli]`) into separate
Evokeds in the same run. For each resulting Evoked, a joint plot is produced with
`Evoked.plot_joint()`, optionally showing topomaps at user-specified peak times.

The app generates:
- One or more Evoked objects (`out_dir/ave.fif`), written together with `mne.write_evokeds`
- A joint plot per condition group (`out_figs/evoked*.png`)
- An HTML QC report (`out_report/report.html`) with the evoked traces and joint plots
- `product.json` summarizing the averaging, with the joint-plot thumbnails embedded

## Inputs

- **`epo`** (`neuro/meeg/mne/epochs`): epoched MEG/EEG data to average (required)

## Outputs

- **`out_dir/ave.fif`** (`neuro/meeg/mne/evoked`): one or more Evoked objects, written with
  `mne.write_evokeds` (`mne.read_evokeds` reads it back as a list when there's more than one)
- **`out_figs/evoked*.png`** (`generic/image/png`): one joint plot per condition group (per
  channel type, if the data has more than one)
- **`out_report/report.html`** (`report/html`): HTML report with all conditions' evoked traces and
  joint plots

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `average_all` | boolean | `false` | If `true`, average all epochs into a single Evoked named `"All"`, ignoring `stimulus_names`/`condition` entirely. |
| `stimulus_names` | string | `""` | Stimulus/condition names to average (used when `average_all` is `false`). To produce several Evokeds in one run, separate independent groups with `;`; within a group, conditions are still pooled together with `,` (e.g. `"face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar"` produces two Evokeds). A value with no `;` is a single group. |
| `condition` | string | `""` | Name(s) for each group in `stimulus_names`, matching 1:1 and `;`-separated the same way (e.g. `"face;scrambled"`). Used as each output Evoked's `comment`. |
| `peaks` | string | `"None"` | Comma-separated time values (seconds) to show topomaps at on the joint plot, applied to every group, e.g. `"0.170,0.300"`. `"None"` uses MNE's automatic peak selection. |

## Usage

### Running on Brainlife.io

1. Select your epoched MEG/EEG dataset as the `epo` input.
2. Set `average_all` to `true` to average all epochs together, or leave it `false` and set
   `stimulus_names`/`condition` to define one or more condition groups.
3. Optionally set `peaks` to choose the topomap times shown on the joint plot.
4. Submit the process.
5. Review the joint plot(s) and HTML report in the output viewer.

### Local Testing

```bash
# Edit config.json to point "epo" at a real epoched .fif file, then:
python main.py
```

## Technical Details

- Uses MNE-Python's `Epochs.average()` to build each Evoked, and `Epochs[stimuli].average()` for
  named condition groups.
- Each Evoked's joint plot is produced with `Evoked.plot_joint()`; with more than one channel type
  (e.g. mag + grad + eeg), it returns one figure per type.
- Generates an interactive QC report with `mne.Report.add_evokeds()`.
- Figure thumbnails embedded in `product.json` are saved at a lower resolution than the
  full-resolution files in `out_figs/`, to stay under the 1MB `product.json` size cap.

## Authors
- Kamilya Salibayeva
- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

- Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
- Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
