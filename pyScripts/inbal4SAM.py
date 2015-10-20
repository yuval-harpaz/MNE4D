__author__ = 'yuval'

cd ~/Data/inbal

import os
import mne
import numpy as np
import surfer
from scipy.io import loadmat

fwd = mne.read_forward_solution('4/4_raw-oct-6-fwd.fif')
pnt=fwd['source_rr']*100
pntPRI=np.copy(pnt)
pntPRI[:,0]=pnt[:,1]
pntPRI[:,1]=-pnt[:,0]

S=pntPRI.shape[0]
f = open("4/SAM/pnt.txt","w") #opens file with name of "test.txt"
f.write(str(S)+'\n')
np.savetxt(f,pntPRI,"%.2f")
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
# sort wts according to A1-A248 order
chanInd=np.array([186,2,46,148,57,150,218,15,14,50,42,66,34,152,154,19,223,224,118,12,120,1,219,85,39,8,101,32,172,162,62,125,188,222,21,159,23,81,10,182,216,87,111,246,74,214,43,241,139,71,206,196,200,133,124,91,89,128,158,129,149,119,48,45,13,86,52,143,176,40,7,41,202,171,105,70,208,60,131,97,166,28,220,122,126,90,192,130,193,217,83,215,9,153,16,88,178,38,76,110,180,113,136,3,68,239,108,165,163,233,234,26,100,17,53,92,190,227,195,95,147,117,183,181,11,151,51,142,209,109,210,114,244,247,103,204,102,5,138,230,94,197,99,231,135,127,189,191,226,156,93,229,184,221,49,141,177,245,144,44,146,238,137,173,35,140,104,61,132,24,167,164,169,55,18,59,47,185,187,75,80,213,115,205,236,67,240,72,96,199,22,201,155,56,161,243,212,211,116,112,170,30,134,36,174,107,25,228,232,98,198,84,123,6,78,248,179,168,65,31,242,69,63,27,160,203,157,20,121,82,73,175,37,77,79,145,207,29,33,106,4,58,194,235,64,237,54,225,])
chanInd=chanInd-1


% gui
% gui wx
# multiply weights by data
source=np.dot(wts[:,chanInd],evoked.data)

# normalize
BL=np.zeros(S)
sourceNorm=np.zeros(source.shape)
for i in range(S):
    #BL[i]=np.abs(np.mean(source[i,0:103]))
    BL[i]=np.mean(np.abs(wts[i,:]))
    sourceNorm[i,:]=np.abs(source[i,:]/BL[i])


brain = surfer.Brain('inbal4', 'both', 'white', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
verticesL=fwd['src'][0]['vertno']
verticesR=fwd['src'][0]['vertno']
dataL=np.abs(sourceNorm[0:fwd['src'][0]['nuse'],388])
dataR=np.abs(sourceNorm[fwd['src'][0]['nuse']:,388])
brain.add_data(dataL, colormap='hot', vertices=verticesL, smoothing_steps=5, hemi='lh')
brain.add_data(dataR, colormap='hot', vertices=verticesL, smoothing_steps=5, hemi='rh')

brain.scale_data_colormap(fmin=0, fmid=np.max([dataL,dataR])/2, fmax=np.max([dataL,dataR]), transparent=True)
#brain.scale_data_colormap(fmin=0, fmid=100, fmax=400, transparent=True)

### SAMNwts ###
# I ran SAMNwts in matlab, sorry, see inbal4SAM.m
Nwts = loadmat('4/SAM/Nwts7')
Nwts=Nwts['Nwts']

source=np.dot(Nwts[:,chanInd],evoked.data)
BL=np.zeros(S)
sourceNorm=np.zeros((S,evoked.data.shape[1]))
for i in range(S):
    #BL[i]=np.mean(source[i,0:103])
    BL[i]=np.mean(np.abs(Nwts[i,:]))
    sourceNorm[i,:]=np.abs(source[i,:]/BL[i])

brain = surfer.Brain('inbal4', 'both', 'white', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
verticesL=fwd['src'][0]['vertno']
verticesR=fwd['src'][0]['vertno']
dataL=sourceNorm[0:fwd['src'][0]['nuse'],388]
dataR=sourceNorm[fwd['src'][0]['nuse']:,388]
brain.add_data(dataL, colormap='hot', vertices=verticesL, smoothing_steps=10, hemi='lh')
brain.add_data(dataR, colormap='hot', vertices=verticesL, smoothing_steps=10, hemi='rh')

brain.scale_data_colormap(fmin=0, fmid=np.max([dataL,dataR])/4, fmax=np.max([dataL,dataR])/2, transparent=True)