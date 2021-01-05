#!/usr/bin/env python
# coding: utf-8

# # HR Dataset

# https://rpubs.com/rhuebner/hr_codebook_v14

# In[91]:


1. Pre-processing
2. Exploratory Data Analysis
3. Findings

# employee personal view - married, gender, status, counts, age
# org structure view - manager, departments, counts
# salary view
# FILTER ONLY NOT RESIGNED
# lead measures view - performance score, engagement surve, latest date perfroamcen
# lag measures - absences, late, resigned or not


# In[203]:


fpath = '/Volumes/data/projects/data/HRDataset_v14.csv'


# In[146]:


import pandas as pd
import numpy as np


# In[147]:


df = pd.read_csv(fpath)


# In[144]:


df


# In[96]:


df.dtypes


# In[97]:


df['Employee_Name'].nunique()


# In[98]:


df['ManagerName'].nunique()


# In[99]:


df['Department'].nunique()


# In[100]:


df.nunique()


# In[101]:




df[["Employee_Name","Department"]].groupby(by=["Department"]).nunique()


# In[102]:


df[df["Department"]=="Admin Offices"]


# In[103]:


df[["DateofHire", "DateofTermination"]] = df[["DateofHire", "DateofTermination"]].apply(pd.to_datetime, format = '%m/%d/%Y')



# In[149]:


df["DOB"] = pd.to_datetime(df['DOB'].str[:-2] + '19' + df['DOB'].str[-2:])


# In[150]:


df.dtypes


# In[153]:


df.groupby(df["DOB"].dt.year).count().plot(kind="bar", legend=False)


# In[107]:


#df[["DOB"]].sort_values(by=['DOB'])

df.groupby(df["DateofHire"].dt.year).count().plot(kind="bar", legend=False)


# In[108]:


df.groupby(df["DateofTermination"].dt.year).count().plot(kind="bar", legend=False)


# In[158]:


df['Age'] = np.datetime64('2020-01-01') - df['DOB']


# In[159]:


df['Age'] = (df['Age'].dt.days/365).astype(np.int64)


# In[160]:


df['Age']


# In[162]:


df[["Employee_Name","DateofTermination"]]


# In[168]:


df[["Employee_Name"]][df['DateofTermination'].isnull()]


# In[170]:


df[df['DateofTermination'].isnull()]


# In[181]:


#1 if resigned, 0 if still employee
df['Resigned'] = np.where(df['DateofTermination'].isnull(), 0, 1)


# In[185]:


df["DateofHire"] = pd.to_datetime(df['DateofHire'])
df["DateofTermination"] = pd.to_datetime(df['DateofTermination'])


# In[201]:


#first condition checks if resigned, then service is resign-hire
df['ServiceLength'] = np.where(df['Resigned']==1, df['DateofTermination'] - df['DateofHire'], np.datetime64('2020-01-01') - df['DateofHire'])


# In[202]:


df['ServiceLength']


# In[206]:


df['ServiceLengthYrs'] = ((df['ServiceLength'].dt.days/365).astype(np.float64))


# In[207]:


df['ServiceLengthYrs']


# In[208]:


np.around(df['ServiceLengthYrs'],2)


# In[ ]:




