#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data


# In[2]:


tasks = pd.read_csv("/Volumes/data/work/picnichealth/tasks.csv")
tasks_group = pd.read_csv("/Volumes/data/work/picnichealth/task_group.csv")
records = pd.read_csv("/Volumes/data/work/picnichealth/records.csv")
timesheet = pd.read_csv("/Volumes/data/work/picnichealth/timesheet_entries.csv")


# # Tasks

# In[3]:


tasks.head()


# In[4]:


tasks = tasks.astype({'created_at': 'datetime64'})
tasks = tasks.astype({'completed_at': 'datetime64'})


# In[5]:


tasks.nunique()


# In[6]:


tasks.task_type.unique()


# In[7]:


tasks.isnull().sum()


# In[8]:


tasks["duration"] = tasks["completed_at"]-tasks["created_at"]


# In[9]:


tasks["total_sec"] = tasks.duration.dt.total_seconds()
tasks["total_hr"] = tasks["total_sec"]/3600


# In[10]:


tasks


# In[ ]:





# In[11]:


grouped = tasks.groupby('task_type')['total_hr']

ave = grouped.apply(lambda x: np.mean(x)).reset_index()
std = grouped.apply(lambda x: np.std(x)).reset_index()
maxim = grouped.apply(lambda x: np.max(x)).reset_index()
minim = grouped.apply(lambda x: np.min(x)).reset_index()


# In[12]:


ave.columns =['task_type', 'ave_duration'] 
std.columns =['task_type', 'std_duration'] 
maxim.columns =['task_type', 'max_duration'] 
minim.columns =['task_type', 'min_duration'] 


# In[13]:


task_counts = tasks.value_counts(["task_type"]).reset_index()
task_counts.columns =['task_type', 'count'] 


# In[14]:


ave_df = pd.DataFrame(ave)
std_df = pd.DataFrame(std)
max_df = pd.DataFrame(maxim)
min_df = pd.DataFrame(minim)
task_counts_df = pd.DataFrame(task_counts)


# In[15]:


max_df = max_df.set_index("task_type")
min_df = min_df.set_index("task_type")
ave_df = ave_df.set_index("task_type")
std_df = std_df.set_index("task_type")
tasks_group = tasks_group.set_index("task_type")
task_counts_df = task_counts_df.set_index("task_type")


# In[ ]:





# In[17]:


task_stat = max_df.join(list([min_df,ave_df,std_df,task_counts_df]))
task_stat["weighted_ave"] = (task_stat["ave_duration"]*task_stat["count"])
task_stat["log_weighted_ave"] = np.log2(task_stat["weighted_ave"]+1) 
task_stat.sort_values(["log_weighted_ave"],ascending=False)


# In[195]:


task_stat = task_stat.reset_index()


# In[196]:



tasks_group.columns


# In[197]:


#task_stat = task_stat.join(tasks_group)

task_stat = task_stat.merge(tasks_group,on='task_type',how='left')


# In[198]:


task_stat


# In[244]:


task_stat = task_stat.sort_values(["log_weighted_ave"],ascending=False)
task_stat
task_stat.to_csv("task_stat.csv")


# In[238]:


#source = data.wheat()
source = task_stat

bars = alt.Chart(source).mark_bar().encode(
    alt.X('log_weighted_ave:O'),
    alt.Color('task_group:N'),
    alt.Y('task_type:N'),
)


text = bars.mark_text(
    align='left',
    baseline='middle',
    dx=8  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='log_weighted_ave'
)




(bars + text).properties(height=900)


# In[245]:


#source = data.wheat()
source = task_stat

bars = alt.Chart(source).mark_bar().encode(
    alt.X('log_weighted_ave:Q'),
    alt.Color('task_group:N'),
    alt.Y('task_type:N'),
)


text = bars.mark_text(
    align='left',
    baseline='middle',
    dx=8  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='log_weighted_ave'
)




(bars + text).properties(height=900)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[18]:


records.head()


# In[248]:


records.columns =['record_id', 'uploaded_at','num_pages'] 
records


# In[250]:



tasks.merge(records,on='record_id',how='left')


# In[ ]:





# In[ ]:





# In[19]:


records.nunique()


# In[20]:


records.isnull().sum()


# In[21]:


timesheet.head()


# In[22]:


timesheet.nunique()


# In[23]:


timesheet.isnull().sum()


# In[24]:


timesheet.head()


# In[25]:


timesheet.drop(timesheet.columns[[5, 6, 7]], axis = 1, inplace = True) 
timesheet.head()


# In[ ]:




