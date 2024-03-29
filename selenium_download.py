import os
import sys

# The wget module
import wget

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib import request
from selenium.common.exceptions import TimeoutException

driver = webdriver.Firefox(executable_path = 'geckodriver.exe') 

start = 1
end = 10000
    
from urllib.error import URLError
    
driver = webdriver.Firefox(executable_path = 'geckodriver.exe')
for x in range(start, end):
    try: 
        # https://www.irctc.co.in/nget/train-search
        driver.get("https://www.irctc.co.in/eticketing/loginHome.jsf")
        
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "captchaImg"))) # waits till the element with the specific id appears
        imgLink = driver.find_element_by_id('captchaImg').get_attribute("src")
        
        #imgLink = imgLink.split('theme1')[0] + 'banner'
        #imgLink = imgLink.split('theme1')[0] + 'banner'
        print(x)
        start = x + 1
        request.urlretrieve(imgLink, 'irct_nlpCatcha\\'+ str(x).zfill(4) +'.png')
    except TimeoutException:
        print("time out error")
        start = start-1
        driver.close()
        driver = webdriver.Firefox(executable_path = 'geckodriver.exe') 
    except URLError:
        print("url error")
        start = start-1
        driver.close()
        driver = webdriver.Firefox(executable_path = 'geckodriver.exe') #