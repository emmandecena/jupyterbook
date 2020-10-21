#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import time
import pandas as pd


# In[2]:


PATH  = "/Volumes/data/projects/web-driver/chromedriver"


# In[3]:


option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
#option.add_argument('--headless')

option.add_experimental_option ('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)



# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})


# In[4]:


driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)

keyword = "electrical"


url = "https://www.seek.co.nz/" + keyword + "-jobs/"

driver.get(url)

jobs = driver.find_elements_by_class_name('_3MPUOLE')


time.sleep(5)
job_list = []

for job in jobs:
    position = job.find_element_by_xpath('//*[@id="app"]/div/div[4]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/article/span[2]/span/h1/a').text 
    #company = job.find_element_by_xpath('//*[@id="app"]/div/div[4]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/article/span[5]').text
    #location = job.find_element_by_xpath('//*[@id="app"]/div/div[4]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/article/div[1]/span[2]/span/strong/span/a').text
    job_item = {
        'position': position,
     #   'company': company,
     #   'location': location,
    }
    job_list.append(job_item)

df = pd.DataFrame(job_list)

print(df)
time.sleep(5)

driver.quit()


# In[5]:


driver.quit()


# In[17]:





# In[ ]:




