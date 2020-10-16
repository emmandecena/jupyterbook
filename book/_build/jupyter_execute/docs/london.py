#!/usr/bin/env python
# coding: utf-8

# # Residential demand data

# In[1]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm


# In[2]:


filepath = "/Volumes/data/projects/data/london-data/london-data.csv"


# In[3]:


df = pd.read_csv(filepath)


# In[4]:


df.head()


# In[ ]:




