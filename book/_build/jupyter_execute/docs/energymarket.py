#!/usr/bin/env python
# coding: utf-8

# # Philippine electricity market
# 
# In this article we explore the current structure of the Philippine electricity market based on the data provided by IEMOP and DOE. 

# ## Data Import
# 
# The data comes from the published market participants list by IEMOP, the electricity market operator of the Philippines.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def get_data(url):
    html_data = pd.read_html(url)
    data = html_data[0]
    return data


# In[3]:


df_wesm = get_data('http://www.iemop.ph/the-market/participants/wesm-members/')


# In[4]:


df_retail = get_data('http://www.iemop.ph/the-market/participants/rcoa-tp/')


# ## Exploratory Data Analysis
# 
# We explore the dataset by looking at each column; looking at unique values, calculating summaries, and plotting distributions.

# ### Wholesale Electricity Spot Market
# 
# This section discusses the data on Wholesale Electricity Spot Market participants.

# First, we look at the column names to see the variables from the data.

# In[5]:


df_wesm.columns


# We get the counts of the unique values in each column.

# In[6]:


df_wesm.nunique()


# #### Participant Name and Short Name
# 
# From the counts above, we notice that `PARTICIPANT NAME` and `SHORT NAME` are not equal. This means that there are duplicate values for these variables. We investigate by performing a cross-tabulation.

# In[7]:


df_cross = pd.crosstab(df_wesm['SHORT NAME'], df_wesm['PARTICIPANT NAME'],margins=True)
df_cross.tail()


# Based on the tabulation, we can see that there are `PARTICIPANT NAME` with multiple `SHORT NAME`.

# In[8]:


df_cross.All[(df_cross.All > 1)].head(n=10)


# We take a look at some of the values.

# In[9]:


df_wesm[df_wesm['SHORT NAME'] =='APRI']


# In[10]:


df_wesm[df_wesm['SHORT NAME'] =='AHC']


# We can see that each `PARTICIPANT NAME` has multiple `RESOURCE` entries. From the inspected data above, we can infer that membership in the spot market is a disaggregation of the power plant units of each participating company.

# #### Region
# 
# We look at the `REGION` variable and see that most of the participants are from Luzon.

# In[11]:


df_wesm.groupby('REGION')['RESOURCE'].nunique()


# We look at the participants with dual regions.

# In[12]:


df_wesm[df_wesm['REGION'] =='LUZON / VISAYAS']


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


# ---

# ### Retail Market
# 
# This section discusses the Retail Market participants.

# In[18]:


df_retail.columns


# In[19]:


df_retail['CATEGORY'].unique()


# In[20]:


df_retail[df_retail['CATEGORY'] =='Retail Electricity Supplier'].head()


# In[ ]:




