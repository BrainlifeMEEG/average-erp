<h1 align="center">average erp</h1>

<p align="center">
  Brainlife.io app: average MEG/EEG epochs into one or more condition ERPs (Evoked)
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.949"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.949-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Brainlife.io app: average MEG/EEG epochs into one or more condition ERPs (Evoked)**

Uses Epochs.average() either on all epochs or on named groups of conditions (';'-separated) to produce one or more Evoked objects, saved together in ave.fif, with a joint plot per group and an HTML report. Use it after epoching to get ERPs/ERFs per condition.

| | |
|---|---|
| **Inputs** | `neuro/meeg/mne/epochs` |
| **Outputs** | `neuro/meeg/mne/evoked` · `generic/image/png` · `report/html` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 1 CPUs · 8 GB memory |
| **Run it** | [doi.org/10.25663/brainlife.app.949](https://doi.org/10.25663/brainlife.app.949) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `evoked` | `neuro/meeg/mne/epochs` | yes | Epoched MEG/EEG data (MNE -epo.fif). |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/evoked` | One or more Evoked objects (ave.fif). |
| `out_figs` | `generic/image/png` | Joint ERP plots per condition group. |
| `out_dir_report` | `report/html` | HTML report with evoked traces and joint plots. |

<details>
<summary><b>Parameters</b> (4)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `average_all` | boolean | `false` | Do you want all of your epoch types/stimuli/conditions to be averaged together? If not, enter the names of the epoch types/stimuli/conditions in the string below. |
| `stimulus_names` | string |  | Stimulus/condition names to average. To produce SEVERAL Evokeds in one run, separate independent groups with ";"; within a group, conditions are still pooled together with "," (e.g. "face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar" produces two Evokeds). A value with no ";" is a single group -- one Evoked, same as before. |
| `condition` | string |  | Name(s) for each group in stimulus_names, matching 1:1 and ";"-separated the same way (e.g. "face;scrambled" for the example above). Used as each output Evoked's label. Just enter the name(s) with no quotation marks. |
| `peaks` | string | `None` | Add a list (comma-separated) of time values at which you would like to display topomaps on a joint ERP plot. |

</details>

<!-- brainlife-app:end -->

## Versions on brainlife.io

This repository hosts several Apps, each built from its own branch.

| App | Branch | Run it | Status |
|---|---|---|---|
| Average ERPs | [`v1.0`](https://github.com/BrainlifeMEEG/average-erp/tree/v1.0) | [doi:10.25663/brainlife.app.949](https://doi.org/10.25663/brainlife.app.949) | current |
| Average ERP (MNE) | [`main`](https://github.com/BrainlifeMEEG/average-erp/tree/main) | [doi:10.25663/brainlife.app.644](https://doi.org/10.25663/brainlife.app.644) | available |

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.949](https://doi.org/10.25663/brainlife.app.949), choose `neuro/meeg/mne/epochs` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/evoked`, `generic/image/png`, `report/html`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository and check out the App's branch (`git checkout v1.0`).
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "epo": "/path/to/evoked/epo",
       "average_all": false,
       "stimulus_names": "",
       "condition": "",
       "peaks": "None"
   }
   ```

3. Run `./main`.

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `average_all` | boolean | `false` | If `true`, average all epochs into a single Evoked named `"All"`, ignoring `stimulus_names`/`condition` entirely. |
| `stimulus_names` | string | `""` | Stimulus/condition names to average (used when `average_all` is `false`). To produce several Evokeds in one run, separate independent groups with `;`; within a group, conditions are still pooled together with `,` (e.g. `"face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar"` produces two Evokeds). A value with no `;` is a single group. |
| `condition` | string | `""` | Name(s) for each group in `stimulus_names`, matching 1:1 and `;`-separated the same way (e.g. `"face;scrambled"`). Used as each output Evoked's `comment`. |
| `peaks` | string | `"None"` | Comma-separated time values (seconds) to show topomaps at on the joint plot, applied to every group, e.g. `"0.170,0.300"`. `"None"` uses MNE's automatic peak selection. |

## Local Testing

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

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Average ERPs. brainlife.io App. [doi:10.25663/brainlife.app.949](https://doi.org/10.25663/brainlife.app.949)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Kamilya Salibayeva
- Maximilien Chaumon (https://github.com/dnacombo)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
