# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 13:14:03 2020

@author: ASUS
"""
#stationarity checking using variogram plot

import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')

df=pd.read_csv('mineral.csv')
df=df[['ID','XCOO','YCOO','Ag']]
df=df[df.ID<800]

import geostatspy.geostats as geostats
# #normalize value
# df['Ag'],tvAg,tnsAg=geostats.nscore(df, 'Ag')

plt.figure()
plt.plot(df.ID,df.Ag,color='k')
plt.title('Ag Field Data')
plt.xlabel('ID')
plt.ylabel('Ag')
plt.show()

x=df.XCOO
y=df.YCOO
z=df.Ag

#visualisasi
import geostatspy.GSLIB as gslib
plt.figure()
cmap = plt.cm.plasma                                    # set the color map
gslib.locmap_st(df,'XCOO','YCOO','Ag',min(x),max(x),min(y),7600000,min(z),max(z),'Ag Distribution','X (m)','','Ag Percentage (%)',cmap)



#make variogram
lag=7000
lag_tol=3000
nlag=30
azi=0
azi_tol=90
bandwidth=9999
lags, gammas, npps = geostats.gamv(df,"XCOO","YCOO","Ag",-9999,9999,lag,lag_tol,nlag,azi,azi_tol,bandwidth,isill=1.0)


#variogram modelling
nug = 0.5
nst = 1 #whether a normal score transformation is used on this variogram
it1 = 1; cc1 = 0.5; azi1 = azi; hmaj1 = 110000; hmin1 = 110000
#it is the type of variogram (Spherical, exponential, gaussian)
#assumption no contribution on minor structure
it2 = 1; cc2 = 0; azi2 = 0; hmaj2 = 9999.9; hmin2 = 400  
xlag=15000
vario = gslib.make_variogram(nug,nst,it1,cc1,azi1,hmaj1,hmin1,it2,cc2,azi2,hmaj2,hmin2) # make model object

index_maj,h_maj,gam_maj,cov_maj,ro_maj = geostats.vmodel(nlag,xlag,azi,vario) 

# plot experimental variogram
plt.figure()                                  
plt.scatter(lags,gammas,color = 'black',s = npps*0.1,label = 'Azimuth ' +str(azi))
plt.plot(h_maj,gam_maj,color = 'black')
plt.legend()
# plt.plot([0,175000],[1.0,1.0],color = 'black')
# plt.plot([0,max(lags)],[1.0,1.0],color = 'black')
plt.xlabel('Lag Distance')
plt.ylabel('Variogram')
plt.title('Ag Distribution Variogram')
plt.xlim([0,175000]); plt.ylim([0,1.5])
# plt.xlim([0,max(lags)]); plt.ylim([0,1.5])
plt.grid()
plt.show()
