# The wget module
import wget

# The BeautifulSoup module
from bs4 import BeautifulSoup
from PIL import Image

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib import request
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import cv2
import numpy as np

from urllib import request

from solve_captchas_with_model_irctc import predictImage
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PIL import Image

def cropImage():
    
    im = Image.open('screenshot.png').convert('L')
    width, height = im.size
    im = im.crop((148, 0, width, height))
    im.save('screenshot.png')
    
def changeColor():
    
    image = cv2.imread('screenshot.png')
    image[np.where((image == image[0,0]).all(axis = 2))] = [255,255,255]
    image[np.where((image > (100,100,100)).all(axis = 2))] = [255,255,255]
    cv2.imwrite('screenshot.png', image)

def makePrediction():
    predictions = predictImage("screenshot.png")
    return predictions

def simpleCaptcha():
    imgLink = driver.find_element_by_class_name('captcha-img').get_attribute("src")
    request.urlretrieve(imgLink, 'screenshot.png')
    image = cv2.imread('screenshot.png')
    print(image[0][0])
    image[np.where((image > (128,128,128)).all(axis = 2))] = (255,0,255)
    image[np.where((image < (128,128,128)).all(axis = 2))] = (255,255,255)
    cv2.imwrite('screenshot.png', image)
    return makePrediction()

def nlpCaptcha():
    imgLink = driver.find_element_by_id('nlpCaptchaImg').get_attribute("src")
    if imgLink.find('theme1') != -1:
        imgLink = imgLink.split('theme1')[0] + 'banner'
    request.urlretrieve(imgLink, 'screenshot.png')
    cropImage()
    changeColor()
    return makePrediction()

def captchaPrediction():
    captchaAnswer = 'captcha'
    predictions = None
    try: 
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "captcha-img")))
        predictions = simpleCaptcha()
    except TimeoutException:
        try: 
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "nlpCaptchaImg")))
            predictions = nlpCaptcha()
            captchaAnswer = 'nlpAnswer'
        except TimeoutException:
            print('unable to find captcha image source file')
            
    captcha = driver.find_element_by_id(captchaAnswer)
    captcha.send_keys(predictions)
    
driver = webdriver.Firefox(executable_path = 'geckodriver.exe') # if you want to use chrome, replace Firefox() with Chrome()
driver.get("https://www.irctc.co.in/nget/train-search")

idName = 'divMain'
try: 
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, idName)))
    print(idName + ' exist')
except TimeoutException:
    print(idName + ' doesnot exist')

driver.find_element_by_link_text('LOGIN').click()

user_name = driver.find_element_by_id('userId')
user_name.send_keys("agamParekh")

password = driver.find_element_by_name('pwd')
password.send_keys("Irctcpass1")

captchaPrediction()

driver.find_elements_by_xpath("//*[contains(text(), 'SIGN IN')]")[0].click()

# second part
try: 
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-inputtext")))
    print("ui-inputtext exist")
except TimeoutException:
    print(idName + ' doesnot exist')

fromStation = driver.find_element_by_class_name("ui-inputtext")
fromStation.click()
fromStation.send_keys('BORIVALI - BVI')

fromStation = driver.find_element_by_xpath("//input[@placeholder='To*']")
fromStation.click()
fromStation.send_keys('SONGADH - SGD')

date = driver.find_element_by_xpath("//input[@placeholder='Journey Date(dd-mm-yyyy)*']")
date.clear()
date.send_keys('21-07-2018')

search = driver.find_elements_by_class_name('search_btn')[0]
search.click()

# third part
try: 
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "check-availability")))
    print("check-availability")
except TimeoutException:
    print(idName + ' doesnot exist')
driver.find_elements_by_id('check-availability')[0].click()

# fourth part
try: 
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "waitingstatus")))
    print("waitingstatus")
except TimeoutException:
    print(idName + ' doesnot exist')
waitingStatus = driver.find_elements_by_class_name('waitingstatus')
print(len(waitingStatus))

for i in range(len(waitingStatus)):
    print(waitingStatus[i].text)
    
book_now_buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Book Now')]")[1:]
print(len(book_now_buttons))
book_now_buttons[0].click()

#

add_passenger_link = driver.find_element_by_link_text('+ Add Passenger')

no_of_passengers = 1
for i in range(no_of_passengers - 1):
    add_passenger_link.click()

psg_name_classes = [
        'form-control.input-xs.ng-touched.ng-dirty.ng-invalid', 
                   'form-control.input-xs.ng-invalid.ng-dirty.ng-touched', 
                  'form-control.ng-touched.ng-dirty.ng-valid',
                  'form-control.input-xs.ng-pristine.ng-invalid.ng-touched'
                  ]
age_classes = [
        'form-control.ng-touched.ng-dirty.ng-invalid',
        'form-control.ng-pristine.ng-invalid.ng-touched',
        'form-control.ng-touched.ng-dirty.ng-invalid',
        'form-control.ng-pristine.ng-invalid.ng-touched'
        ]

gender_classes = [
        'form-control.ng-star-inserted.ng-dirty ng-valid ng-touched',
        'form-control.ng-pristine.ng-invalid.ng-star-inserted.ng-touched',
        'form-control.ng-pristine.ng-invalid.ng-star-inserted.ng-touched',
        'form-control.ng-pristine.ng-invalid.ng-star-inserted.ng-touched'        
        ]
passenger_name = ['Agam Parekh', 'Karan shah']
passenger_age = ['23', '24']
gender = ['1','1']

for i in range(no_of_passengers):
    driver.find_element_by_class_name(psg_name_classes[1]).click()
    driver.find_element_by_class_name(psg_name_classes[1]).send_keys('S')

psgn_name = driver.find_element_by_id('psgn-name')
psgn_name.send_keys('Agam Parekh')

age = driver.find_element_by_xpath("//input[@placeholder='Age']")
age.send_keys('23')
source_code = driver.page_source
print(source_code[:50])
classGender = source_code[:source_code.find('formcontrolname="passengerGender"')]
classGender = classGender[classGender.rfind('class="') + 6:].replace('\"', '').replace('\'', '').strip().replace(' ', '.')
    
from selenium.webdriver.support.ui import Select
select_gender = Select(driver.find_element_by_class_name(classGender))
#Male 1 Female 2
select_gender.select_by_index(1)

# not working for refreshingt
driver.find_element_by_xpath("//div[@class='nlpRefresh' and contains(@onclick,'nlpAjaxCaptcha')]").click()

captchaPrediction()
driver.find_elements_by_xpath("//*[contains(text(), 'Continue Booking ')]")[0].click()


# Review Booking
driver.find_element_by_xpath("//*[contains(text(), 'Continue Booking')]").click()

#set firebase session true
cred = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://captchadetection-8351e.firebaseio.com/'
})

root = db.reference()
root.child('paytm').update({'session' : True})

#Payment
driver.find_element_by_link_text('Wallets / Cash Card').click()
#
driver.find_elements_by_xpath("//*[contains(text(), 'Paytm Wallet')]")[0].click()
make_payment_btns = driver.find_elements_by_xpath("//*[contains(text(), 'Make Payment')]")
print(len(make_payment_btns))
for make_payment_btn in make_payment_btns:
    if make_payment_btn.is_displayed():
        print(make_payment_btn.get_attribute("class"))
        print(make_payment_btn.text)
        make_payment_btn.click()
              
# log in 
driver.find_element_by_id('otp-btn').click()

#Enter mobile number
driver.switch_to_frame('login-iframe')
driver.find_element_by_id('mobile').send_keys('8898037271')
driver.find_element_by_class_name('btn-primary-new').click()

#

    

value = root.child('paytm').get('otp')
otp = value[0]['otp']
print(otp)
driver.find_element_by_id('mobile').send_keys(otp)
driver.find_element_by_class_name('btn-primary-new').click()