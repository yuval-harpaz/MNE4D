__author__ = 'yuval'
import numpy as np
import noamParallel
from datetime import datetime as dt
import time
def ourfun(q):
    print(q)
    time.sleep(2)
    print('done '+str(q))

a=np.random.rand(40,40000)
jobs = 10
params = []
for ii in range(jobs):
    params.append(ii)

print(dt.now())
map_results = noamParallel.parmap(ourfun, params, 6)
print(dt.now())
#print(map_results)



