#!/usr/bin/env python
# coding: utf-8

# # Philippine electricity market

# {badge}`python3,badge-success` {badge}`case study,badge-secondary` {badge}`electricity market,badge-warning` 

# This article provides an **exploratory data analysis** on the Philippine electricity market by comparing the data provided by IEMOP and DOE on their websites.
# 
# The first part explores the **Wholesale Electricity Spot Market** while second part explores the **Retail Electricity Spot Market**. Finally, we compare the published data from the DOE, IEMOP and WESM.

# ## Data Import
# 
# The data comes from the published market participants list by IEMOP, the electricity market operator of the Philippines.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


t_props = [
  ('font-size', '80%')
  ]
   
styles = [
  dict(selector="th", props=t_props),
  dict(selector="td", props=t_props)
  ]


# In[3]:


def get_data(url):
    html_data = pd.read_html(url)
    data = html_data[0]
    return data


# In[4]:


df_wesm = get_data('http://www.iemop.ph/the-market/participants/wesm-members/')


# In[5]:


df_retail = get_data('http://www.iemop.ph/the-market/participants/rcoa-tp/')


# ## Exploratory Data Analysis
# 
# We explore the dataset by looking at each column; looking at unique values, calculating summaries, and plotting distributions.

# ### Wholesale Electricity Spot Market
# 
# This section discusses the data on Wholesale Electricity Spot Market participants.

# First, we look at the column names to see the variables from the data. We get the counts of the unique values in each column.

# In[6]:


df_wesm.nunique()


# #### Participant Name and Short Name
# 
# From the counts above, we notice that `PARTICIPANT NAME` and `SHORT NAME` are not equal. This means that there are duplicate values for these variables. We investigate by performing a cross-tabulation.

# In[7]:


df_cross = pd.crosstab(df_wesm['SHORT NAME'], df_wesm['PARTICIPANT NAME'],margins=True)
df_cross.tail().style.set_table_styles(styles)


# Based on the tabulation, we can see that there are `PARTICIPANT NAME` with multiple `SHORT NAME`.

# In[8]:


df_cross.All[(df_cross.All > 1)].head(n=10)


# We take a look at some of the values.

# In[9]:


df_wesm[df_wesm['SHORT NAME'] =='APRI'].tail().style.set_table_styles(styles)


# In[10]:


df_wesm[df_wesm['SHORT NAME'] =='AHC'].tail().style.set_table_styles(styles)


# We can see that each `PARTICIPANT NAME` has multiple `RESOURCE` entries. From the inspected data above, we can infer that membership in the spot market is a disaggregation of the power plant units of each participating company.

# #### Region
# 
# We look at the `REGION` variable and see that most of the participants are from Luzon.

# In[11]:


df_wesm.groupby('REGION')['RESOURCE'].nunique()


# We look at the participants with dual regions.

# In[12]:


df_wesm[df_wesm['REGION'] =='LUZON / VISAYAS'].tail().style.set_table_styles(styles)


# Except for the NGCP, which is a transmission company and NPC, all the participants with dual regions are Aggregators (WAG) with 'ceased' status. ERC has issued a circular to stop the operation of all WAGs.

# #### Category
# 
# Just like any market, we can see that WESM participants are either buyers or sellers of electricity.

# In[13]:


df_wesm['CATEGORY'].unique()


# #### Membership
# 
# Participants have either `DIRECT` or `INDIRECT` membership, which pertains to their grid connection status.

# In[14]:


df_wesm['MEMBERSHIP'].unique()


# #### Effective Date
# 
# Date when they participated in the market. We convert the data type.

# In[15]:


df_wesm = df_wesm.astype({'EFFECTIVE DATE': 'datetime64'})


# In[16]:


g1 = df_wesm.groupby(['REGION', 'CATEGORY', 'EFFECTIVE DATE', 'STATUS']).count().reset_index()
g1 = g1[g1['REGION']!='LUZON / VISAYAS']


# #### Visualisations

# In[17]:


import plotly.express as px

fig = px.scatter(g1, x='EFFECTIVE DATE', y='RESOURCE', range_y=['0','25'], color = 'CATEGORY',facet_row="REGION")
fig.update_xaxes(rangeslider_visible=False)
fig.show()


# In[18]:


names = df_wesm.apply(lambda col: str(col['PARTICIPANT NAME']) + ' ' + str(col['RESOURCE']), axis=1)


# In[19]:


import os

import googlemaps

gmap = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))


# In[20]:


# Geocoding an address
df_wesm_coded = pd.DataFrame({"PLACE":names[0:400]})
df_wesm_coded["LAT"] = None
df_wesm_coded["LON"] = None
geocode_result = []

for i in range(0, len(names[0:400]),1):
    geocode_result = gmap.geocode(names[i])
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        df_wesm_coded.iat[i,df_wesm_coded.columns.get_loc("LAT")] = lat
        df_wesm_coded.iat[i,df_wesm_coded.columns.get_loc("LON")] = lon
    except Exception as e:
        lat = None
        lon = None
        #print('Error, skipping address...', e)


# In[21]:


df_wesm_coded = df_wesm_coded[df_wesm_coded['LON'].notnull()]


# In[22]:


import gmaps


# In[23]:


gmaps.configure(api_key=os.getenv('GOOGLE_API_KEY'))


map_df = df_wesm_coded[['LAT','LON']]

scatter_layer = gmaps.symbol_layer(
    map_df, fill_color='green', stroke_color='green', scale=2
)
fig = gmaps.figure(zoom_level=5, center=(12.8797, 121.7740))
fig.add_layer(scatter_layer)


# In[24]:


fig


# ---

# ### Retail Market
# 
# This section discusses the Retail Market participants.

# In[25]:


df_retail.columns


# In[26]:


df_retail['CATEGORY'].unique()


# In[27]:


df_retail[df_retail['CATEGORY'] =='Contestable Customer'].head().style.set_table_styles(styles)


# In[ ]:





# In[ ]:





# In[ ]:




