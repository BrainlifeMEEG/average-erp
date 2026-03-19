# app-average-erp

Brainlife App to create an Evoked data structure, given an Epochs object and conditions to use for averaging.

1) Input file is: 
    * `fname` data file for the Epochs object
2) Input string is:
    * 'stimulus names' list of strings, each string is one of the stimulus names to use for averaging
    * 'condition' a string to use for the condition name in the Evoked object
3) Input boolean is:
    * 'average all' if true, average all epochs in the Epochs object, regardless of the stimulus name

4) Ouput files are:
    * `ave/fif`
    * HTML report
    * Figure of the evoked data


## Authors
- Kamilya Salibayeva (ksalibay@iu.edu)

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
