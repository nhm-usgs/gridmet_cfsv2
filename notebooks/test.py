import gridmet_cfsv2 as gm
import  numpy as np
m = gm.Gridmet(type=0)
ds = m.tmin
ds.head()
print(m.list_cache())
tmp = 0
ds2 = m.tmin
print(ds2.head())
print(np.min(ds2))
print(np.max(ds2))