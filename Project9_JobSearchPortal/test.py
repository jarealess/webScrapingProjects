from selenium import webdriver
import time



option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
#option.add_argument("headless")
option.add_argument('--log-level=3')
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option)
browser.get('http://www.elempleo.com/co/ofertas-empleo/?trabajo=datos')


time.sleep(5)

## ----------------------- Results per pages
n_results = browser.find_element_by_class_name('form-control.js-results-by-page')

browser.execute_script("arguments[3].click();",n_results)
time.sleep(5)

browser.close()