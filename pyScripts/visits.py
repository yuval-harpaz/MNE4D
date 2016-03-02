import numpy as np
import surfer
#cd ~/Data/epilepsy/b134b/2
cd ~/Data/epilepsy/b391/3

stcL=np.load('stcL.npy')
stcR=np.load('stcR.npy')
verticesL=np.load('verticesL.npy')
verticesR=np.load('verticesR.npy')

%gui
%gui wx

subject = 'b391'
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"

brain = surfer.Brain(subject, 'both', 'pial',
                     views='lateral', subjects_dir=subjects_dir)
brain.add_data(stcL, colormap='hot',
               vertices=verticesL, smoothing_steps=10,  hemi='lh')
brain.add_data(stcR, colormap='hot',
               vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brain.scale_data_colormap(
    fmin=maxval/4, fmid=maxval / 2, fmax=maxval, transparent=True)