# MNE4D
running MNE on 4D-neuroimaging data
install MNE python on linux, clone the repo at https://github.com/mne-tools/mne-python
to convert 4D data such as 'c,rfhp0.1Hz' to fif file use Denis' function mne_bti2fiff.py
from linux terminal run something like this:
mne_bti2fiff.py -p c,rfDC -o test_raw.fif
for the terminal to find the faunction add the commands folder to its path, I did it by adding to .bashrc this line:
export PATH=/home/yuval/mne-python/mne/commands:$PATH
