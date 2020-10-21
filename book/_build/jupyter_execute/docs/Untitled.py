#!/usr/bin/env python
# coding: utf-8

# In[ ]:


driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)

keyword = "electrical"

url = "https://www.jobstreet.com.ph/en/job-search/" + keyword + "-jobs/"

driver.get(url)

jobs = driver.find_elements_by_class_name('FYwKg _17IyL_6 _2-ij9_6 _3Vcu7_6 MtsXR_6')

time.sleep(5)
job_list = []

for job in jobs:
    position = job.find_element_by_xpath('//*[@id="jobList"]/div[2]/div[3]/div/div[1]/div/div/article/div/div/div[1]/div[1]/div[2]/h1/a/div').text 
    company = job.find_element_by_xpath('//*[@id="jobList"]/div[2]/div[3]/div/div[1]/div/div/article/div/div/div[1]/div[1]/div[2]/span').text
    location = job.find_element_by_xpath('//*[@id="jobList"]/div[2]/div[3]/div/div[1]/div/div/article/div/div/div[1]/div[1]/span[1]/span').text
    salary = job.find_element_by_xpath('//*[@id="jobList"]/div[2]/div[3]/div/div[1]/div/div/article/div/div/div[1]/div[1]/span[2]').text
    
    job_item = {
        'position': position,
        'company': company,
        'location': location,
        'salary': salary,  
    }

    job_list.append(job_item)

df = pd.DataFrame(job_list)

print(df)
time.sleep(5)

driver.quit()


# In[ ]:


driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)
driver.get("https://www.seek.com.au/")


searchTitle = driver.find_element_by_id("keywords-input")
searchTitle.send_keys("electrical")
searchTitle.send_keys(Keys.RETURN)

#searchLocation = driver.find_element_by_id("locationAutoSuggest-aria-description")


print(searchTitle.text())


time.sleep(5)


driver.quit()


# In[ ]:





# In[ ]:


Volumes(/data/projects/data/brazil/df_task.csv)

