from os import chdir
import os.path
import numpy as np
from termcolor import colored
import mne

snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
vertices_to = [np.arange(10242), np.arange(10242)]
for sub in subjects:
    fsSub='alice'+sub[0].upper()+sub[1:]
    chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    if  os.path.isfile('nat_fsa-lh.stc'):
        print colored(sub,'red'),colored('/MNE/nat_fsa-lh.stc exists','blue')
    else:
        print colored('working on '+sub,'blue')
        fname_inv = sub+'_raw-oct-6-meg-inv.fif'
        fname_evoked='nat-ave.fif'
        evoked = mne.read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
        inverse_operator = mne.minimum_norm.read_inverse_operator(fname_inv)
        stc = mne.minimum_norm.apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
        stc.save('nat_orig')
        #morph_mat=np.load('morph_mat.npy')
        morph_mat = mne.compute_morph_matrix(fsSub, 'fsaverage', stc.vertno, vertices_to)
        np.savez('test',data = morph_mat.data ,indices=morph_mat.indices, indptr =morph_mat.indptr, shape=morph_mat.shape )
        stc = mne.morph_data_precomputed(fsSub, 'fsaverage', stc, vertices_to, morph_mat)
        #stc = mne.morph_data(fsSub, 'fsaverage', stc, grade=vertices_to, n_jobs=3)
        #stc_to = mne.morph_data(subject_from, 'fsaverage', stc, n_jobs=1, grade=vertices_to)
        stc.save('nat_fsa')
           
