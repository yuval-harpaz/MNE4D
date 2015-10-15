__author__ = 'yuval'

# cd /home/yuval/Data/inbal
import os
import mne
import numpy as np
import surfer
cd ~/Data/inbal
fwd = mne.read_forward_solution('4/4_raw-oct-6-fwd.fif')
pnt=fwd['source_rr']*100
S=pnt.shape[0]
f = open("4/pnt.txt","w") #opens file with name of "test.txt"
f.write(str(S)+'\n')
np.savetxt(f,pnt,"%.2f")
f.close()

os.system("SAMcov64 -r 4 -d rs,xc,hb,lf_c,rfhp0.1Hz -m aud -v")
os.system("SAMwts64 -r 4 -d rs,xc,hb,lf_c,rfhp0.1Hz -m aud -c Aa -t pnt.txt -v")
# dump the weights into text file and put them in np array
os.system("~/MNE4D/pyScripts/readwts.py 4/SAM/pnt.txt.wts > 4/SAM/wts.txt")
with open('4/SAM/wts.txt') as f:
    content = f.readlines()
content=content[1:]
wts=np.zeros((S,248))
for i in range(S):
    for j in range(248):
        wts[i,j]=float(content[i*248+j])
# read the averaged data
evoked = mne.read_evokeds('4/4aud-ave.fif', condition=0, baseline=(-0.2, 0))
# multiply weights by data
source=np.dot(wts,evoked.data)
# normalize
BL=np.zeros(S)
sourceNorm=source
for i in range(S):
    BL[i]=np.mean(source[i,0:103])
    sourceNorm[i,:]=np.abs(sourceNorm[i,:]/BL[i])

% gui
% gui wx
brain = surfer.Brain('inbal4', 'both', 'white', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
verticesL=fwd['src'][0]['vertno']
verticesR=fwd['src'][0]['vertno']
dataL=sourceNorm[0:fwd['src'][0]['nuse'],388]
dataR=sourceNorm[fwd['src'][0]['nuse']:,388]
brain.add_data(dataL, colormap='hot', vertices=verticesL, smoothing_steps=10, hemi='lh')
brain.add_data(dataR, colormap='hot', vertices=verticesL, smoothing_steps=10, hemi='rh')

brain.scale_data_colormap(fmin=0, fmid=np.max([dataL,dataR])/4, fmax=np.max([dataL,dataR])/2, transparent=True)


