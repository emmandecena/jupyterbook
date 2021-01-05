#!/usr/bin/env python
# coding: utf-8

# # Human Resources Analytics

# {badge}`python3,badge-success` {badge}`case study,badge-secondary` {badge}`human resources,badge-warning` 

# ## Introduction
# 
# As organizations continue to grow and optimize its human resources, to acknowledge the differences that arise in the workplace that affect daily activities in terms of employee moral, productivity, and turnover rates.
# 
# To identify and understand these differences in the heirarchy of the organization, leaders need a framework in which to strategize HR objectives such as staffing estimates, forecasting, retention, training and compensation.
# 
# **This article demonstrates an analytics framework for HR data to provide a comprehensive overview of an organization's workforce.**
# 
# What we will cover:
# 
# 1. **Pre-processing:** To prepare and clean the dataset for EDA
# 2. **Exploratory Data Analysis:** To investigate variable relationships
# 3. **Findings:** To highlight and dig deeper on the key relationships found
# 4. **Assumption Testing:** To check if the data meets the statistical assumptions requirements.
# 
# **Dataset:** We use the synthetic dataset designed by Drs. Rich Huebner and Carla Patalano (https://rpubs.com/rhuebner/hr_codebook_v14) which was created specifically for a case study in the college that they teach at.
# ***

# ## Pre-processing
# 
# This section contains:
# 
# - **Inspect each variable** for data types and missing values
# - **Filter redundant variables** to remove irrelevant data
# - **Cleaning ambiguous data** by replacement to uniform
# - **Address missing data** by imputation or filtering
# - **Convert each variable** to proper data type 
# - **Create calculated variables** from existing ones
# 

# In[1]:


# employee personal view - married, gender, status, counts, age
# org structure view - manager, departments, counts
# salary view
# FILTER ONLY NOT RESIGNED
# lead measures view - performance score, engagement surve, latest date perfroamcen
# lag measures - absences, late, resigned or not


# In[2]:


import pandas as pd
import numpy as np
fpath = '/Volumes/data/projects/data/HRDataset_v14.csv'
df = pd.read_csv(fpath)


# In[3]:


# dataframe styles
t_props = [
  ('font-size', '80%')
  ]
   
styles = [
  dict(selector="th", props=t_props),
  dict(selector="td", props=t_props)
  ]


# ### Inspecting the variables

# In[4]:


# checking for variable names
df.columns


# In[5]:


df.info(memory_usage='deep')


# In[6]:


df.head().style.set_table_styles(styles)


# ### Filtering irrelevant
# 
# We look at unique counts to see redundancy, seems like `EmpID`,  `DeptID`, `PositionID`,`ManagerID`, `MaritalStatusID`, `MarriedID` are redundant

# In[7]:


df.nunique()


# In[8]:


# Position has multiple PositionID, might signify rank or levels
df[['Position','PositionID']].groupby('Position').nunique()


# In[9]:


df[df['Position']=='Software Engineer'][['Employee_Name','Position','PositionID']]


# In[10]:


df['MaritalStatusID']


# In[11]:


df['MaritalDesc'].unique()


# ### Dropping columns

# In[12]:


dropCols = ['EmpID', 'EmpStatusID','DeptID', 'PositionID','ManagerID', 'MaritalStatusID', 'MarriedID']

df.drop(columns=dropCols, inplace=True)
df


# ### Cleaning ambiguous data

# In[13]:


df['HispanicLatino'].unique()
df['HispanicLatino'] = df['HispanicLatino'].replace(to_replace=['No', 'Yes', 'no', 'yes'], value=[0, 1, 0, 1])
df['HispanicLatino'].unique()


# ### Address missing data
# 
# `DateofTermination` contains 207 missing values which means that 207 out

# In[14]:


#checking for missing data
df.isnull().sum()


# ### Converting and downcasting data types

# In[15]:


# Converting to datetime 
dateVariables = ['LastPerformanceReview_Date', 'DateofHire', 'DateofTermination']
df[dateVariables] = df[dateVariables].apply(pd.to_datetime, format = '%m/%d/%Y')

# Adjusting for century in two-digit years
df["DOB"] = pd.to_datetime(df['DOB'].str[:-2] + '19' + df['DOB'].str[-2:])

# Converting to boolean
boolVariables = ['Termd','HispanicLatino']
df[boolVariables] = df[boolVariables].astype('bool')

# Converting to categorical
catVariables = ['GenderID', 'PerfScoreID', 'FromDiversityJobFairID', 'Position', 'State','Sex','MaritalDesc', 'CitizenDesc', 'RaceDesc','TermReason', 'EmploymentStatus', 'Department', 'ManagerName', 'RecruitmentSource', 'PerformanceScore']
df[catVariables] = df[catVariables].astype('category')

# Converting and downcasting to int/float
intVars = ['Salary', 'Zip', 'EmpSatisfaction', 'SpecialProjectsCount', 'DaysLateLast30', 'Absences']
floatVars = ['EngagementSurvey']

df[intVars].apply(pd.to_numeric, downcast='unsigned')


df[intVars] = df[intVars].apply(pd.to_numeric, downcast='unsigned')
df[floatVars] = df[floatVars].apply(pd.to_numeric, downcast='float')


# In[16]:


df.info(memory_usage='deep')


# ### Create calculated variables

# In[17]:


df['Age'] = np.datetime64('2020-01-01') - df['DOB']
df['Age'] = (df['Age'].dt.days/365).astype(np.uint8)


# In[18]:


#True if resigned, False if still employee
df['Resigned'] = np.where(df['DateofTermination'].isnull(), False, True)


# In[19]:


#first condition checks if resigned, then service is resign-hire
df['ServiceLength'] = np.where(df['Resigned']==1, df['DateofTermination'] - df['DateofHire'], np.datetime64('2020-01-01') - df['DateofHire'])
df['ServiceLengthYrs'] = ((df['ServiceLength'].dt.days/365).astype(np.float32))
df['ServiceLengthYrs'] = np.around(df['ServiceLengthYrs'],2)


# In[20]:


df


# ## Exploratory Data Analysis
# 
# This section contains:
# 
# - **Inspect distributions of dates** 
# - **Summary of ints and floats**
# 

# In[21]:


df.groupby(df["DOB"].dt.year).count().plot(kind="bar", legend=False)


# In[22]:


#df[["DOB"]].sort_values(by=['DOB'])

df.groupby(df["DateofHire"].dt.year).count().plot(kind="bar", legend=False)


# In[23]:


df.groupby(df["DateofTermination"].dt.year).count().plot(kind="bar", legend=False)


# In[24]:


df[["Employee_Name","DateofTermination"]]


# In[25]:


df[["Employee_Name"]][df['DateofTermination'].isnull()]


# In[26]:


df[df['DateofTermination'].isnull()]


# In[206]:





# In[ ]:




