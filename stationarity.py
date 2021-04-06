# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:34:54 2020

@author: ASUS
"""
#stationarity checking using swath plot

import pandas as pd
import matplotlib.pyplot as plt



df=pd.read_csv('mineral.csv')
df=df[['ID','XCOO','YCOO','Ag']]
df=df[df.ID<800]

# import geostatspy.geostats as geostats
# #normalize value
# df['Ag'],tvAg,tnsAg=geostats.nscore(df, 'Ag')

plt.figure()
plt.plot(df.ID,df.Ag,color='k')
plt.title('Ag Field Data')
plt.xlabel('ID')
plt.ylabel('Ag')
plt.show()

from scipy import stats
slope, intercept, corrcoeff, p_value, stderr  = stats.linregress(df.ID,df.Ag)

m=slope
c=intercept

df.Y=m*df.ID+c

plt.figure()
plt.plot(df.ID,df.Ag,color='k') #point plotting
plt.plot(df.ID,df.Y,linewidth=3.5,color='y',label='trend') #trend plotting
plt.title('Ag Field Data')
plt.xlabel('ID')
plt.ylabel('Ag')
plt.legend()
plt.show()

#sampling at certain ID
df_part=df.iloc[503:573]

slope, intercept, corrcoeff, p_value, stderr  = stats.linregress(df_part.ID,df_part.Ag)

m=slope
c=intercept

df_part.Y=m*df_part.ID+c

plt.figure()
plt.plot(df_part.ID,df_part.Ag,color='k')
plt.plot(df_part.ID,df_part.Y,linewidth=3.5,color='y',label='trend')
plt.title('Ag Field Data')
plt.xlabel('ID')
plt.ylabel('Ag')
plt.show()

#outlier detection using IQR
Q3 = df.Ag.describe().T['75%']
Q1 = df.Ag.describe().T['25%']
IQR = Q3 - Q1

upper_fence = Q3 + (1.5 * IQR)
lower_fence = Q1 - (1.5 * IQR)

df_out=df[(df.Ag < lower_fence) | (df.Ag > upper_fence)]

# plt.figure()
# plt.plot(df_out.Ag)
# plt.show()

