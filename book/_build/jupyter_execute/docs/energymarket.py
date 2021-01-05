#!/usr/bin/env python
# coding: utf-8

# # Energy Industry Overview

# {badge}`python3,badge-success` {badge}`case study,badge-secondary` {badge}`electricity market,badge-warning` 

# Working with these files can be a challenge, especially given their heterogeneous nature. Some preprocessing is required before they are ready for consumption by your CNN.
# 
# Fortunately, I participated in the LUNA16 competition as part of a university course on computer aided diagnosis, so I have some experience working with these files. At this moment we top the leaderboard there :)
# 
# **This article provides an exploratory data analysis on the Philippine electricity market by comparing the data provided by IEMOP and DOE on their websites.**
# 
# What we will cover:
# 
# 1. **Pre-processing:** and adding missing metadata
# 2. **Exploratory Data Analysis:** and what tissue these unit values correspond to
# 3. **Resampling** to an isomorphic resolution to remove variance in scanner resolution.
# 
# **Dataset:** The HR Dataset was designed by Drs. Rich Huebner and Carla Patalano to accompany a case study designed for graduate HR students studying HR metrics, measurement, and analytics. The students use Tableau data visualization software to uncover insights about the case. This is a synthetic data set created specifically to go along with the case study (proprietary for the college that we teach at). https://rpubs.com/rhuebner/hr_codebook_v14
# 
# ***
# 

# ## Data Extraction
# 
# The data comes from the published market participants list by IEMOP, the electricity market operator of the Philippines.

# Cache the data; check if extracted is equal to imported, if not get the difference, then run the geocoding

# In[329]:


# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt


# In[330]:


# Formatting of DataFrame html view
t_props = [
  ('font-size', '80%')
  ]
   
styles = [
  dict(selector="th", props=t_props),
  dict(selector="td", props=t_props)
  ]


# In[331]:


def get_data(url):
    html_data = pd.read_html(url)
    data = html_data[0]
    return data


# In[332]:


df_wesm = get_data('http://www.iemop.ph/the-market/participants/wesm-members/')
# Dropping 451 Team Sual NA Resource value
df_wesm = df_wesm.dropna()


# In[333]:


df_retail = get_data('http://www.iemop.ph/the-market/participants/rcoa-tp/')
df_retail = df_retail.dropna()


# In[334]:


# load a simple dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()

alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)


# In[335]:


df_wesm.describe()


# In[336]:


df_retail.describe()


# In[337]:


df_wesm.dtypes


# ### Exploratory Data Analysis
# 
# We explore the dataset by looking at each column; looking at unique values, calculating summaries, and plotting distributions.

# ### Wholesale Electricity Spot Market
# 
# This section discusses the data on Wholesale Electricity Spot Market participants.

# First, we look at the column names to see the variables from the data. We get the counts of the unique values in each column.

# #### Participant Name and Short Name
# 
# From the counts above, we notice that `PARTICIPANT NAME` and `SHORT NAME` are not equal. This means that there are duplicate values for these variables. We investigate by performing a cross-tabulation.

# In[338]:


df_cross = pd.crosstab(df_wesm['SHORT NAME'], df_wesm['PARTICIPANT NAME'],margins=True)
df_cross.tail().style.set_table_styles(styles)


# Based on the tabulation, we can see that there are `PARTICIPANT NAME` with multiple `SHORT NAME`.

# In[339]:


df_cross.All[(df_cross.All > 1)].head(n=10)


# We take a look at some of the values.

# In[340]:


df_wesm[df_wesm['SHORT NAME'] =='APRI'].tail().style.set_table_styles(styles)


# In[341]:


df_wesm[df_wesm['SHORT NAME'] =='AHC'].tail().style.set_table_styles(styles)


# We can see that each `PARTICIPANT NAME` has multiple `RESOURCE` entries. From the inspected data above, we can infer that membership in the spot market is a disaggregation of the power plant units of each participating company.

# #### Region
# 
# We look at the `REGION` variable and see that most of the participants are from Luzon.

# In[342]:


df_wesm.groupby('REGION')['RESOURCE'].nunique()


# In[343]:


df_retail.groupby('REGION')['NAME'].nunique()


# We look at the participants with dual regions.

# In[344]:


df_wesm[df_wesm['REGION'] =='LUZON / VISAYAS'].tail().style.set_table_styles(styles)


# In[345]:


df_retail[df_retail['REGION'] =='Luzon/Visayas']


# In[346]:


df_retail[df_retail['REGION'] =='Visayas']


# Except for the NGCP, which is a transmission company and NPC, all the participants with dual regions are Aggregators (WAG) with 'ceased' status. ERC has issued a circular to stop the operation of all WAGs.

# In[347]:


df_wesm = df_wesm[df_wesm['REGION']!='LUZON / VISAYAS']


# In[348]:


df_wesm.describe()


# #### Category
# 
# Just like any market, we can see that WESM participants are either buyers or sellers of electricity.

# In[349]:


df_wesm['CATEGORY'].unique()


# #### Membership
# 
# Participants have either `DIRECT` or `INDIRECT` membership, which pertains to their grid connection status.

# In[350]:


df_wesm['MEMBERSHIP'].unique()


# #### Effective Date
# 
# Date when they participated in the market. We convert the data type.

# In[351]:


df_wesm = df_wesm.astype({'EFFECTIVE DATE': 'datetime64'})


# In[352]:


df_retail = df_retail.astype({'EFFECTIVE DATE': 'datetime64'})


# In[353]:


df_wesm


# #### Status
# 
# We only consider participants with `REGISTERED` status

# In[354]:


df_wesm['STATUS'].unique()


# In[355]:


df_retail['STATUS'].unique()


# In[356]:


df_wesm = df_wesm[df_wesm['STATUS']=='REGISTERED']
df_retail = df_retail[df_retail['STATUS']=='Registered']


# In[357]:


df_wesm['STATUS'].unique()


# In[358]:


df_retail['STATUS'].unique()


# In[359]:


df_wesm = df_wesm.drop(['STATUS'],axis=1)
df_retail = df_retail.drop(['STATUS'],axis=1)


# #### Visualisations

# In[360]:


import os
import googlemaps
gmap = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))


# In[ ]:





# In[361]:


# Reset index since the rows dropped caused the index to skip integer sequence
df_wesm = df_wesm.reset_index(drop=True)


# In[362]:


df_wesm.isnull().sum()


# In[363]:


# Geocoding an address
#df_wesm_coded = pd.DataFrame({"PLACE":names})
df_wesm["LAT"] = None
df_wesm["LON"] = None
country_limit = {'country': 'Philippines'}
geocode_result = []

for i in range(0, len(df_wesm.index),1): 
    geocode_result = gmap.geocode(df_wesm['RESOURCE'][i],country_limit)
    
    if geocode_result: #meaning its successful
        pass
    else:
        geocode_result = gmap.geocode(df_wesm['PARTICIPANT NAME'][i] + ' ' + df_wesm['RESOURCE'][i],country_limit)

    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        df_wesm.iat[i,df_wesm.columns.get_loc("LAT")] = lat
        df_wesm.iat[i,df_wesm.columns.get_loc("LON")] = lon
    except Exception as e:
        #IndexError
        lat = None
        lon = None


# In[364]:


df_wesm


# In[366]:


df_wesm.to_csv('/Volumes/data/projects/data/philippine-energy-market/wholesale_participants.csv', index=False)


# In[367]:


df_wesm[df_wesm['LON'].isnull()]


# In[368]:


df_wesm['LON'].isnull().sum()


# In[ ]:





# In[ ]:





# In[ ]:





# ---

# ### Retail Market
# 
# This section discusses the Retail Market participants.

# In[25]:


df_retail.columns


# In[373]:


df_retail['CATEGORY'].unique()


# In[ ]:





# In[372]:


df_retail[df_retail['CATEGORY'] =='Contestable Customer'].head().style.set_table_styles(styles)


# In[382]:


# Removing non-ascii character on line 380
df_retail['NAME'] = df_retail["NAME"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))


# In[383]:


# Reset index since the rows dropped caused the index to skip integer sequence
df_retail = df_retail.reset_index(drop=True)


# In[386]:


df_retail.describe


# In[387]:


df_retail.isnull().sum()


# In[388]:


# Geocoding an address
df_retail["LAT"] = None
df_retail["LON"] = None
country_limit = {'country': 'Philippines'}
geocode_result = []

for i in range(0, len(df_retail.index),1): 
    geocode_result = gmap.geocode(df_retail['NAME'][i],country_limit)
    
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        df_retail.iat[i,df_retail.columns.get_loc("LAT")] = lat
        df_retail.iat[i,df_retail.columns.get_loc("LON")] = lon
    except Exception as e:
        #IndexError
        lat = None
        lon = None


# In[389]:


df_retail


# In[390]:


i


# In[391]:


df_retail.to_csv('/Volumes/data/projects/data/philippine-energy-market/retail_participants.csv', index=False)


# In[410]:


df_retail_null = df_retail[df_retail['LON'].isnull()]
df_retail_null = df_retail_null.reset_index(drop=True)


# In[ ]:





# In[411]:


df_retail_null.groupby('REGION')['NAME'].nunique()


# In[412]:


df_retail_null.groupby('CATEGORY')['NAME'].nunique()


# In[413]:


df_retail_null[df_retail_null["CATEGORY"]=="Retail Electricity Supplier"]


# In[ ]:


df.columns = df.columns.str.replace(' ', '_')


# In[414]:


df_retail_null['NAME'] = df_retail_null['NAME'].str.strip()  # or .replace as above


# In[415]:


#Limited to 2,500 API calls per day
df_retail_null


# In[437]:


gmap.geocode(df_retail_null['NAME'][1] +' '+ 'Philippines')


# In[435]:


df_retail_null['NAME'][1] +' '+ 'Philippines'


# In[429]:


country_limit = {'country': 'Philippines'}


# In[ ]:




