from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator

data_path = sample.data_path()
fname = data_path
fname += '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'
