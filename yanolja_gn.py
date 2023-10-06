import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# 창원
url = 'https://www.yanolja.com/motel/r-910053?lat=37.50681&lng=127.06624&advert=AREA&topAdvertiseMore=0&sort=133&placeListType=motel&pathDivision=r-910053'
#url = 'https://www.naver.com/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

res = requests.get(url, headers=headers)
html = BeautifulSoup(res.text, 'lxml')
print(html)

from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")
#options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
#options.add_argument("--disable-dev-shm-usage")

chrome = webdriver.Chrome(options=options)
chrome.implicitly_wait(5)

chrome.get(url)
time.sleep(2)
html = BeautifulSoup(chrome.page_source, 'lxml')

div0 = 'PlaceListBody_listGroup__LddQf'
div1 = 'PlaceListBody_itemGroup__1V8Q3 PlaceListBody_textUnitList__HEDb3'
div2 = 'PlaceListItemText_container__fUIgA text-unit'
i=0

for i in range(1,4,1):
    chrome.find_element(By.CLASS_NAME, f'{div0} div:nth-child({i}) a').click()
    time.sleep(1)

    chrome.find_element(By.CLASS_NAME, 'css-1i028dt').click()
    time.sleep(1)


print(len(html.select(f'div.{div1}')))
print(f'{div1} div:nth-child(3) a')