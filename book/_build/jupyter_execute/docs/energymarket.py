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

html_wesm = pd.read_html('http://www.iemop.ph/the-market/participants/wesm-members/')
html_retail = pd.read_html('http://www.iemop.ph/the-market/participants/rcoa-tp/')
df_wesm = html_wesm[0]
df_retail = html_retail[0]


# ## Exploratory Data Analysis
# 
# We explore the dataset by looking at each column; looking at unique values, calculating summaries, and plotting distributions.

# ### Wholesale Electricity Spot Market
# 
# This section discusses the Wholesale Electricity Spot Market participants.

# In[2]:


df_wesm.columns


# In[3]:


df_wesm.nunique()


# In[4]:


df_wesm.nunique()


# In[5]:


df_cross = pd.crosstab(df_wesm['SHORT NAME'], df_wesm['PARTICIPANT NAME'],margins=True)
df_cross.head()


# In[6]:


df_cross.All[(df_cross.All > 1)].head()


# In[7]:


df_wesm[df_wesm['SHORT NAME'] =='APRI']


# In[8]:


df_wesm[df_wesm['SHORT NAME'] =='AHC']


# In[9]:


df_wesm.groupby('REGION')['RESOURCE'].nunique()


# In[10]:


df_wesm['CATEGORY'].unique()


# In[11]:


df_wesm[df_wesm['CATEGORY'] =='WAG']


# ---

# ### Retail Market
# 
# This section discusses the Retail Market participants.

# In[12]:


df_retail.columns


# In[13]:


#df_retail[df_retail['CATEGORY'] =='WAG']
df_retail['CATEGORY'].unique()


# In[14]:


df_retail[df_retail['CATEGORY'] =='Retail Electricity Supplier']


# In[ ]:




