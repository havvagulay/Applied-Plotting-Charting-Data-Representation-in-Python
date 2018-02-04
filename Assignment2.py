
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
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
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import calendar

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))
    
    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')

noaa = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

# find highs
noaahigh = noaa.where(noaa['Element'] == 'TMAX')
noaahigh.dropna(axis = 0, how='any', inplace=True)
noaahigh['Year'] = noaahigh['Date'].apply(lambda e: (e[:4]))
noaahigh['Month-Day'] = noaahigh['Date'].apply(lambda e: (e[-5:]))

#cleanup high data
noaahigh = noaahigh[noaahigh['Month-Day'] != '02-29']
noaahigh15 = noaahigh[noaahigh['Year'] == '2015']
noaahigh = noaahigh[noaahigh['Year'] != '2015']


dfhigh = noaahigh.groupby('Month-Day').aggregate({'Data_Value' : max})
dfhigh15 = noaahigh15.groupby('Month-Day').aggregate({'Data_Value' : max})

#find lows
noaalow = noaa.where(noaa['Element'] == 'TMIN')
noaalow.dropna(axis = 0, how='any', inplace=True)
noaalow['Year'] = noaalow['Date'].apply(lambda e: (e[:4]))
noaalow['Month-Day'] = noaalow['Date'].apply(lambda e: (e[-5:]))


#cleanup low data
noaalow = noaalow[noaalow['Month-Day'] != '02-29']
noaalow15 = noaalow[noaalow['Year'] == '2015']
noaalow = noaalow[noaalow['Year'] != '2015']


dflow = noaalow.groupby('Month-Day').aggregate({'Data_Value' : min})
dflow15 = noaalow15.groupby('Month-Day').aggregate({'Data_Value' : min})

# temp is given by tenths of degrees C, convert to C
dflow['Data_Value'] = dflow['Data_Value'] / 10
dfhigh['Data_Value'] = dfhigh['Data_Value'] / 10
dflow15['Data_Value'] = dflow15['Data_Value'] / 10
dfhigh15['Data_Value'] = dfhigh15['Data_Value'] / 10

dflow.reset_index(inplace = True)
dfhigh.reset_index(inplace = True)
dflow15.reset_index(inplace = True)
dfhigh15.reset_index(inplace = True)

brokenlow = dflow15[dflow15['Data_Value'] < dflow['Data_Value']] 
brokenhigh = dfhigh15[dfhigh15['Data_Value'] > dfhigh['Data_Value']]

plt.figure(figsize=(20,8))
plt.plot(dfhigh['Data_Value'], '#ffba00', label='Record highs for 2005-2014')
plt.plot(dflow['Data_Value'], '#0080FF', label='Record lows for 2005-2014')

plt.gca().fill_between(range(len(dfhigh.values)), 
                       dfhigh['Data_Value'], dflow['Data_Value'], 
                       facecolor='#e1e1e1', 
                       alpha=0.3)

plt.scatter( brokenhigh.index.values, brokenhigh['Data_Value'], s=30, c = '#e61d35', label = 'Record highs broken in 2015')
plt.scatter( brokenlow.index.values, brokenlow['Data_Value'], s=30, c = '#0F52BA', label= 'Record lows broken in 2015')

# add a label to the x axis
plt.xlabel('Day of the Year')
# add a label to the y axis
plt.ylabel('Temperature ($^\circ$C)')
# add a title
plt.title('Temperature Summary for Ann Arbor, Michigan, United States (2005-2014) and 2005')
#add legend
plt.legend()

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.xticks(np.arange(12), calendar.month_name[1:13] )

days = [0]
sumdays = 0
for month in range(1, 13):
    days.append(calendar.monthrange(2001, month)[1] + sumdays - 1)
    sumdays += calendar.monthrange(2001, month)[1]

plt.gca().xaxis.set_major_locator(plt.FixedLocator(range(15, 360, 30)))
plt.gca().xaxis.set_minor_locator(plt.FixedLocator(days))

plt.grid(which='minor', alpha=0.2)


# In[ ]:




# 
