# The selenium module
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib import request
import speech_recognition as sr

driver = webdriver.Firefox(executable_path = 'geckodriver.exe') # if you want to use chrome, replace Firefox() with Chrome()

driver.get("https://www.irctc.co.in/nget/train-search")
driver.find_element_by_link_text('LOGIN').click()
try: 
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'nlpAnswer')))
    print('nlpAnswer' + ' exist')
except TimeoutException:
    print('nlp answer doesnot exist')
    
driver.execute_script("document.getElementsByClassName('nlpSound')[0].click()")

source_code = driver.page_source
audio_file_link = source_code[source_code.find('<audio '): source_code.find('</audio>')].split('src')[1][2:-2]
print(audio_file_link)
request.urlretrieve(audio_file_link, 'captcha.wav')

user_name = driver.find_element_by_id('userId')
user_name.send_keys("agamParekh")

password = driver.find_element_by_name('pwd')
password.send_keys("Irctcpass1")

with open("CaptchaDetectionGoogle.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()    
r = sr.Recognizer() 
# Load audio file
with sr.AudioFile('captcha.wav') as source:
    audio = r.record(source)
# Transcribe audio file
text = r.recognize_google(audio)
print(text)
 