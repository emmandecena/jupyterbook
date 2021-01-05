#!/usr/bin/env python
# coding: utf-8

# # Numpy exercise

# Numpy is 
# 
# - Dimensions
# - Slicing

# {cite}`285005`

# In[1]:


import numpy as np


# Initializing arrays - pass list

# In[2]:


x = np.arange(10)
x


# In[21]:


b = np.array([np.arange(4), np.arange(4,8),np.arange(8,12)])
b


# In[29]:


c = b[:,np.newaxis]
c


# In[37]:


c.shape


# In[46]:


c[2,:,1]


# In[43]:


c[2]


# In[28]:


d = b[np.newaxis,:]
d


# In[35]:





# In[36]:


d.shape


# In[2]:


x = np.array([[[ 0,  1,  2,  3],
               [ 4,  5,  6,  7],
               [ 8,  9, 10, 11]],

              [[12, 13, 14, 15],
               [16, 17, 18, 19],
               [20, 21, 22, 23]]])


# In[33]:


x.shape


# In[35]:


x


# In[41]:





# In[ ]:





# In[ ]:





# Normalize x such that each of its rows, within each sheet, will sum to a value of 1. Make use of the sequential function np.sum, which should be called only once, and broadcast-division.
# 
# 

# In[45]:


xsum = np.sum(x, axis=(2))
xsum


# In[46]:


xsum.shape


# In[49]:


x/xsum[...,np.newaxis]


# In[87]:


images = np.random.rand(500, 48, 48, 3)
imgsmall = np.random.rand(3, 4, 4, 3)
imgsmall[0][0]
#stores as a single array


# Using the sequential function np.max and broadcasting, normalize images such that the largest value within each color-channel of each image is 1.

# In[81]:


imgsmall[0][0][1]


# In[89]:


np.max(imgsmall, axis=(1,2))


# In[ ]:





# In[ ]:





# ## Bibliography
# 
# ```{bibliography} ../_bibliography/references.bib
# :style: plain
# :filter: docname in docnames
# ```

# In[ ]:




