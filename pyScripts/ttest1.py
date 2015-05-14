from os import chdir
import os.path
from termcolor import colored
#from surfer.io import read_stc
from mne import read_source_estimate

#subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
subjects = ['idan', 'inbal']
counter=0

for sub in subjects:
	#fsSub='alice'+sub[0].upper()+sub[1:]
	chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
	stc = read_source_estimate('mne_dSPM_inverse')
     list_stc[counter]=stc.data
     counter=counter+1






#if  os.path.isfile('mne_dSPM_inverse-lh.stc'):
#		print colored(sub,'red'),colored('/MNE/mne_dSPM_inverse-lh.stc exists','blue')
#	else:
#		print colored('working on '+sub,'blue')
#		fname_inv = sub+'_raw-oct-6-meg-inv.fif'
#		if os.path.isfile(fname_inv):
#			print('okay')
#		else:
#			print colored(sub+' no inv!!!','red')
#		fname_evoked=sub+'ftWbW-ave.fif'
#		evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
#		inverse_operator = read_inverse_operator(fname_inv)
#		stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
#		stc.save('mne_%s_inverse' % method)
	
