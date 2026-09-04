# app-average-erp

Brainlife App to create one or more Evoked (ERP/ERF) data structures from an Epochs object, given
one or more named groups of conditions to average.

1) Input file is:
    * `epo` data file for the Epochs object
2) Input strings are:
    * `stimulus_names` — the stimulus/condition names to average. To produce **several** Evokeds in
      one run, separate independent groups with `;`; within a group, conditions are still pooled
      together with `,` (unchanged meaning). Example:
      `face/famous,face/unfamiliar;scrambled/famous,scrambled/unfamiliar` produces two Evokeds, one
      pooling the two face conditions, one pooling the two scrambled conditions. A value with no `;`
      is a single group — identical to giving just one condition list.
    * `condition` — a name for each group above, matching 1:1, `;`-separated the same way (e.g.
      `face;scrambled` for the example above). Used as each output Evoked's `comment`.
    * `peaks` — comma-separated time values (seconds) to show topomaps at on the joint plot, applied
      to every group, or `None` for MNE's automatic peak selection.
3) Input boolean is:
    * `average_all` — if true, average **all** epochs into a single Evoked named `"All"`, ignoring
      `stimulus_names`/`condition` entirely.

4) Output files are:
    * `out_dir/ave.fif` — one or more Evoked objects (`mne.write_evokeds`, `mne.read_evokeds` reads
      it back as a list when there's more than one)
    * `out_figs/evoked*.png` — one joint plot per condition (per channel type, if the data has more
      than one)
    * HTML report with all conditions' evoked traces and joint plots


## Authors
- Kamilya Salibayeva (ksalibay@iu.edu)

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
