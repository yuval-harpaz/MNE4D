from os import chdir
import os.path
from termcolor import colored
from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator
from mne import read_evokeds
from mne.minimum_norm import apply_inverse, read_inverse_operator


snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
for sub in subjects:
	fsSub='alice'+sub[0].upper()+sub[1:]
	chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
	if  os.path.isfile('mne_dSPM_inverse-lh.stc'):
		print colored(sub,'red'),colored('/MNE/mne_dSPM_inverse-lh.stc exists','blue')
	else:
		print colored('working on '+sub,'blue')
		fname_inv = sub+'_raw-oct-6-meg-inv.fif'
		if os.path.isfile(fname_inv):
			print('okay')
		else:
			print colored(sub+' no inv!!!','red')
		fname_evoked=sub+'ftWbW-ave.fif'
		evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
		inverse_operator = read_inverse_operator(fname_inv)
		stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
		stc.save('mne_%s_inverse' % method)
	
