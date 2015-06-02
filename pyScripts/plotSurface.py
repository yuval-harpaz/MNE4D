
from surfer import Brain

%gui
%gui wx
brain = Brain('fsaverage', 'both', 'pial', views='caudal', subjects_dir = '/usr/local/freesurfer/subjects')
