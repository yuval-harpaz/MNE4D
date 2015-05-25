 # ipython --gui=wx
from os import chdir
import os.path
from termcolor import colored
#from surfer.io import read_stc
from mne import read_source_estimate
from scipy.stats import ttest_1samp as ttest
from surfer import Brain
import numpy as np
filePref='nat_fsa'
time0=0.075
time1=0.125
const=4 #ttest_1samp(X,constant)

subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
counter=0
XX=np.empty([8,20484])
for sub in subjects:
    X=[]
    #fsSub='alice'+sub[0].upper()+sub[1:]
    chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    stc = read_source_estimate(filePref)
    samp0=np.abs(stc.times - time0).argmin()
    samp1=np.abs(stc.times - time1).argmin()
    X=stc.data[0:20484,samp0:samp1]
    Xm=X.mean(1)
    XX[counter,0:20484]=Xm
    counter+=1
XXm=XX.mean(0)
XXmL=XXm[0:10242]
XXmR=XXm[10242:20484]
brain = Brain('fsaverage', 'both', 'pial', views='caudal', subjects_dir = '/usr/local/freesurfer/subjects')
brain.add_data(XXmL, colormap='hot', vertices=np.arange(10242), smoothing_steps=10, hemi='lh')
brain.add_data(XXmR, colormap='hot', vertices=np.arange(10242), smoothing_steps=10, hemi='rh')
brain.scale_data_colormap(fmin=0, fmid=XXm.max()/2, fmax=XXm.max(), transparent=True)
# statistics
results=ttest(XX,const) # results: row 0 = t, raw 1 = p

posP=results[1]
posP[np.where(results[0]<=0)]=1
notSig=np.where(posP<=0.1) # one tailed, positive t only

posT=results[0]
posT[notSig]=0
#posT[np.where(results[0]<0)]=0
#posT[np.where(results[1]>=0.1)]=0
brain1 = Brain('fsaverage', 'both', 'pial', views='caudal', subjects_dir = '/usr/local/freesurfer/subjects')
brain1.add_data(posT[0:10242], colormap='hot', vertices=np.arange(10242), smoothing_steps=1, hemi='lh')
brain1.add_data(posT[10242:20484], colormap='hot', vertices=np.arange(10242), smoothing_steps=1, hemi='rh')
maxT=posT.max()
brain1.scale_data_colormap(fmin=0, fmid=maxT/2, fmax=maxT, transparent=True)





#if  os.path.isfile('mne_dSPM_inverse-lh.stc'):
#        print colored(sub,'red'),colored('/MNE/mne_dSPM_inverse-lh.stc exists','blue')
#    else:
#        print colored('working on '+sub,'blue')
#        fname_inv = sub+'_raw-oct-6-meg-inv.fif'
#        if os.path.isfile(fname_inv):
#            print('okay')
#        else:
#            print colored(sub+' no inv!!!','red')
#        fname_evoked=sub+'ftWbW-ave.fif'
#        evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
#        inverse_operator = read_inverse_operator(fname_inv)
#        stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
#        stc.save('mne_%s_inverse' % method)
    
