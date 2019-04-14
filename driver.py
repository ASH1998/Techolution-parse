#imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import timestring
from datetime import datetime

#base url
url = "https://techolution.app.param.ai/jobs/"

#load selenium driver
# using headless chrome driver.
#the chromedriver.exe should be in path or in the same dir.
option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)
print("PHANTOM LOAD COMPLETE")

#--------------------------------------------------------------------
def get_jobs(driver):
    '''
    param driver : selenium driver object

    This method takes in selenium driver object and returns 
    jobs(list of jobs) and soup object for the page.

    '''
    #driver.implicitly_wait(30)
    driver.get(url)
    #get bs4 object of the page
    soup_level1=BeautifulSoup(driver.page_source, 'lxml')
    jobs = []
    date = 0
    for i in soup_level1.find_all('h3'):
        try:
            x = str(i).split('>')[1]
            jobs.append([x.split('<')[0], date])
        except Exception as e:
            print("err on ", e)
            continue
    #a = driver.find_element_by_class_name("date_posted")
    return jobs, soup_level1

#---------------------------------------------------------------------

#call the jobs method
jobs, soup_level1 = get_jobs(driver)
print(len(jobs))

#if there is some problem, like internet or some bug when carrying out url parse
if len(jobs)<3:
    i = 1
    while(True):
        i +=1
        print(len(jobs))
        print("going ", i, " round")
        jobs, soup_level1 = get_jobs(driver)
        if len(jobs)>3:
            break
        if i>200:
            print("GET A POWERFUL NET CONNECTION...")
            break
        
print(jobs)
#close the driver
driver.quit()

#convert soup object to str to get dates.
soupp = str(soup_level1)

all_dates = []
for j in soupp.split('''<span class="date_posted" data-v-5b44ba93="">'''):
    all_dates.append(j.split('<')[0])

print(len(all_dates))
print(all_dates)
all_dates.pop(0)
all_jobs = jobs[2:]

# assert if the length of jobs and dates are same.
assert(len(all_jobs) == len(all_dates))

#change all string of dates(like '3 months ago' ) into datetime object.
datee = []
for u in all_dates:
    datee.append(str(timestring.Range(u)).split(' ')[1])
d = [datetime.strptime(i, '%m/%d/%y') for i in datee]
for i in range(len(all_jobs)):
    all_jobs[i][1] = d[i]

#creating a pandas dataframe
df = pd.DataFrame(all_jobs, columns=["JOB TITLE", "DATE"])
#sorting by ascending order of date.
df = df.sort_values(by='DATE')
#view the final dataframe.
print(df)
#save the dataframe into csv file.
df.to_csv("Techolution.csv")