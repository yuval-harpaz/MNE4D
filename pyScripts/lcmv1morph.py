from os import chdir as cd
from os.path import isfile
import mne
import numpy as np
import pickle
from termcolor import colored
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
vertices_to = [np.arange(10242), np.arange(10242)]
for sub in subjects:
    #X=[]
    fsSub='alice'+sub[0].upper()+sub[1:]
    cd('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    stc_orig=mne.read_source_estimate('lcmv_orig')
    # stcF = lcmv(evoked1, fwdFixed, noise_cov, data_cov, reg=0.01,pick_ori='normal')
    vertices=np.arange(10242)
    #stc = mne.morph_data(fsSub, 'fsaverage', stc_orig, grade=5,subjects_dir='/usr/local/freesurfer/subjects') # beware with n_jobs on PyCharm
    if  isfile('morph_mat.p'):
        print colored(sub+' reading morph_mat','green')
        morph_mat = pickle.load( open( "morph_mat.p", "rb" ) )
    else:
        print colored(sub+' has no morph_mat, computing ','red')
        morph_mat = mne.compute_morph_matrix(fsSub, 'fsaverage', stc_orig.vertno, vertices_to, subjects_dir='/usr/local/freesurfer/subjects')
        pickle.dump(morph_mat,open('morph_mat.p','w'))
    stc_fsa = mne.morph_data_precomputed(fsSub, 'fsaverage', stc_orig, vertices_to, morph_mat)
    #stc_to = mne.morph_data(subject_from, 'fsaverage', stc, n_jobs=1, grade=vertices_to)
    stc_fsa.save('lcmv_fsa')
