from os import chdir as cd
from os.path import isfile
import mne
import numpy as np
import pickle
from termcolor import colored
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
vertices_to = [np.arange(10242), np.arange(10242)]
sub='idan'
fsSub='alice'+sub[0].upper()+sub[1:]
cd('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
stc_orig=mne.read_source_estimate('lcmv_orig')
vertices=np.arange(10242)
stc = mne.morph_data(fsSub, 'fsaverage', stc_orig, grade=5,subjects_dir='/usr/local/freesurfer/subjects',n_jobs=2) # beware with n_jobs on PyCharm
