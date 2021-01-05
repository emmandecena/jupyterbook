#!/usr/bin/env python
# coding: utf-8

# # Residential Electricity Consumption

# {badge}`python3,badge-success` {badge}`case study,badge-secondary` {badge}`load profiles,badge-warning` 

# In this article we explore the electricity load profiles of residential households in the London area. The data comes from the public data release of the UK’s dynamic time-of-use electricity pricing trial {cite}`schofield2015low`. It was a part of the Low Carbon London project which involved subjecting 5,478 anonymised households in the London area to an experimental dynamic time-of-use tariff for 2013.

# ## Exploratory data analysis
# 
# The households had smart-meters installed, and electricity consumption measurements were taken at half-hour intervals for the whole year. The daily load profile used in the analysis was calculated by taking the mean daily consumption of each household in half-hourly intervals.
# 
# The data also labeled each household according to the electricity tariff type it received: standard tariff or dynamic tariff. The customers on the dynamic tariff were issued three pricing signals and their corresponding time of day application through a text message or the Smart Meter in-home display. In contrast, the customers on standard tariff were charged with a flat rate. 
# 
# Finally, the households were grouped according to socioeconomic status groupings provided by Acorn categories. Acorn is a geodemographic segmentation of the UK’s population. The dataset contains three grouping levels in descending order of socio-economic status: Affluent, Comfortable, and Adversity. 
# 
# The Acorn classification is also used to ensure that the households under standard and dynamic tariffs were approximately representatives of London. 

# 
# In this section we dig deeper into the dataset, creating visualisations and summary measures that would give us a better understanding of the data.

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


filepath = "/Volumes/data/projects/data/london-data/london-data.csv"


# Reading the file and checking the column names

# In[3]:


df = pd.read_csv(filepath)
df.columns


# We need to append zeros to the time variable for correct sorting when melted

# In[4]:


df.rename(columns=lambda x: '00' + x if (len(x) == 1) else ('0' + x if (len(x) == 2) else x), inplace=True)
df.columns


# In[5]:


pd.crosstab(df.TARIFF, df.ACORN_GROUPED,margins=True)


# In[6]:


dfmelt = df.melt(id_vars=('HOUSEHOLD', 'ACORN', 'ACORN_GROUPED', 'TARIFF'),var_name='TIME', value_name='kWH')
dfmelt.head()


# In[7]:


g1 = dfmelt.groupby(['ACORN_GROUPED','ACORN', 'TIME']).mean().reset_index()
g1.head()


# In[8]:


import plotly.express as px

fig = px.line(g1, x='TIME', y='kWH', color='ACORN_GROUPED',line_group="ACORN")
fig.show()


# ## Bibliography
# 
# ```{bibliography} ../_bibliography/references.bib
# :style: plain
# :filter: docname in docnames
# ```
