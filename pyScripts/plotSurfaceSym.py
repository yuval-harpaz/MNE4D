


%gui
%gui wx
from surfer import Brain
from scipy.io import loadmat
import numpy as np
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