import pickle
from surfer import Brain
from scipy.io import loadmat
import numpy as np

%gui
%gui wx

brain = Brain('fsaverage_sym', 'both', 'pial', views='caudal', subjects_dir = '/usr/local/freesurfer/subjects')
cd /home/yuval/Copy/MEGdata/alice/idan/MNE
mat = loadmat('R100.mat')
R=mat['R']
mat = loadmat('/usr/local/freesurfer/subjects/fsaverage_sym/surf/pairs.mat')
verticesL=mat['lPair']
verticesR=mat['rPair']
vertices=np.arange(10242)
vertices[:]=verticesL
brain.add_data(R[0:10242], colormap='hot', vertices=vertices, smoothing_steps=10, hemi='lh')
vertices[:]=verticesR
brain.add_data(R[10242:20484], colormap='hot', vertices=vertices, smoothing_steps=10, hemi='rh')


morph_mat = pickle.load( open( "morph_mat.p", "rb" ) )
vertices_to = [np.arange(10242), np.arange(10242)]
mne.compute_morph_matrix('aliceIdan', 'fsaverage_sym', stc_orig.vertno, vertices_to, subjects_dir='/usr/local/freesurfer/subjects')
pickle.dump(morph_mat,open('morph_mat.p','w'))