
from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator
from mne import read_evokeds
from mne.minimum_norm import apply_inverse, read_inverse_operator
fname_evoked='ft_WbW-ave.fif'
fname_inv = 'ohad_raw-oct-6-meg-inv.fif' 
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)


# Load data
evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
inverse_operator = read_inverse_operator(fname_inv)

stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
stc.save('mne_%s_inverse' % method)

# morph to fsaverage

import mne
import numpy as np
from mne.datasets import sample
subject_from = 'aliceOhad'
subject_to = 'fsaverage'
fname='mne_dSPM_inverse'
stc_from = mne.read_source_estimate(fname)
vertices_to = [np.arange(10242), np.arange(10242)]
stc_to = mne.morph_data(subject_from, subject_to, stc_from, n_jobs=1, grade=vertices_to)
stc_to.save('%s_wbw-meg' % subject_to)

## Morph using another method -- useful if you're going to do a lot of the
## same inter-subject morphing operations; you could save and load morph_mat
#morph_mat = mne.compute_morph_matrix(subject_from, subject_to, stc_from.vertno,vertices_to)

#stc_to_2 = mne.morph_data_precomputed(subject_from, subject_to, stc_from, vertices_to, morph_mat)
#stc_to_2.save('%s_audvis-meg_2' % subject_to)



