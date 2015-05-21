from os import chdir
import os.path
from termcolor import colored
import mne
import numpy as np
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
vertices_to = [np.arange(10242), np.arange(10242)]
for sub in subjects:
    fsSub='alice'+sub[0].upper()+sub[1:]
    chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    if  os.path.isfile('mne_dSPM_fsa-lh.stc'):
        print colored(sub,'red'),colored('/MNE/mne_dSPM_fsa-lh.stc exists','blue')
    else:
        print colored('working on '+sub,'blue')
        subject_from='alice'+sub[0].upper()+sub[1:]
        stc = mne.read_source_estimate('mne_dSPM_inverse')
        if  os.path.isfile('morph_mat.npy'):
            print colored(sub+' reading morph_mat','green')
            #np.load('morph_mat.npy')
            loader = np.load('test.npz')
        else:
            print colored(sub+' has no morph_mat, computing ','red')
            morph_mat = mne.compute_morph_matrix(subject_from, 'fsaverage', stc.vertno, vertices_to)
            #np.save('morph_mat',morph_mat)
            np.savez('test',data = morph_mat.data ,indices=morph_mat.indices, indptr =morph_mat.indptr, shape=morph_mat.shape )
        stc = mne.morph_data_precomputed(subject_from, 'fsaverage', stc, vertices_to, morph_mat)
        #stc_to = mne.morph_data(subject_from, 'fsaverage', stc, n_jobs=1, grade=vertices_to)
        stc.save('mne_dSPM_fsa')

    
