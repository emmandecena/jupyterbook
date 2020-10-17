#!/usr/bin/env python
# coding: utf-8

# # Philippine electricity market
# 
# In this article we explore the current structure of the Philippine electricity market based on the data provided by IEMOP and DOE.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize

html_wesm = pd.read_html('http://www.iemop.ph/the-market/participants/wesm-members/')
html_retail = pd.read_html('http://www.iemop.ph/the-market/participants/rcoa-tp/')


# In[2]:


df_wesm = html_wesm[0]
df_wesm.head()


# In[3]:


df_retail = html_retail[0]
df_retail.head()


# In[ ]:




