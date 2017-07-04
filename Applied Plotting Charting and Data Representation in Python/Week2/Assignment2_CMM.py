
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/c63364120150e33d2ed8234706ea4b1b71228c47757b5a972b0d451c.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **San Diego, California, United States**, and the stations the data comes from are shown on the map below.

# In[57]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
from datetime import datetime
import os

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'c63364120150e33d2ed8234706ea4b1b71228c47757b5a972b0d451c')


# In[9]:

#Get date and sort by date
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/c63364120150e33d2ed8234706ea4b1b71228c47757b5a972b0d451c.csv')

by_date=df.sort_values(['Date','Data_Value'],ascending=[True,False])
by_date.head(5)


# In[10]:

#Remove Leap Days
df['Year'], df['Month-Date'] = zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))
df = df[df['Month-Date'] != '02-29']
df.head(5)


# In[11]:

#sort by date and temperature
by_date_temp=df.sort_values(['Month-Date','Data_Value'],ascending=[True,True])
by_date_temp.head(10)


# In[18]:

#extract min/max data from dataframe
temp_min = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
temp_max = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})
temp_min.head(20)
temp_max.head(20)    


# In[19]:

#extract min and max for temp data for 2015
temp_min_2015 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
temp_max_2015 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})
temp_min_2015.head(20)
temp_max_2015.head(20)


# In[20]:

#extract datat when min or max temp was broken in 2015
broke_min=np.where(temp_min_2015['Data_Value']<temp_min['Data_Value'])[0]
broke_max=np.where(temp_max_2015['Data_Value']>temp_max['Data_Value'])[0]


# In[21]:

broke_max, broke_min


# In[61]:

#create a plot
plt.figure()
plt.figure(figsize=(15,7))

#add series to plot
plt.plot(temp_min.values, 'b', label = 'Record Low (2005-2014)')
plt.plot(temp_max.values, 'r', label = 'Record High (2005-2014)')

#plot broken high/low temperatures
plt.scatter(broke_min,temp_min_2015.iloc[broke_min], c='c', label= "Broke Record Low - 2015")
plt.scatter(broke_max,temp_max_2015.iloc[broke_max], c='y', label= "Broken Record High - 2015")

#set Axis
plt.gca().axis([-5, 370, -300, 500])
plt.xticks(range(0, len(temp_min), 20), temp_min.index[range(0, len(temp_min), 20)], rotation = '45', fontsize=12)
plt.yticks(fontsize=12)

#fill between plots
plt.gca().fill_between(range(len(temp_min)), temp_min['Data_Value'], temp_max['Data_Value'], facecolor = 'magenta', alpha = 0.08)

#Label Chart
plt.xlabel('Day of the Year (MM-DD)', fontsize=12)
plt.ylabel('Temperature (Tenths of Degrees C)', fontsize=12)
plt.title('Temperature High/Lows near San Diego,CA between 2005-2015',fontsize=15)
plt.legend(loc=4, frameon = True)

#LETS SEE IT!!!!
plt.show()

#Save as .PNG file
#my_path = os.path.abspath('C:\Users\marech\Desktop')
#plt.figure().savefig('Assignment2_CMM.png')




