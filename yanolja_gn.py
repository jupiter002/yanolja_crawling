import requests
from bs4 import BeautifulSoup
import time
from selenium import *
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
div2 = 'PlaceListItemText_container__fUIgA'



i=1

review_sep = []
while i<5: # 숙소개수만큼 반복
    try:
        chrome.find_element(By.CLASS_NAME, f'{div0} div:nth-child({i}) a').click() # 상세페이지 들어가기
        time.sleep(2)

        print(chrome.find_element(By.CLASS_NAME, 'css-t9rim1').text) # 숙소명
        time.sleep(2)
        chrome.find_element(By.CLASS_NAME, 'css-1iizn56 button:nth-child(2)').click() # 위치버튼 클릭
        time.sleep(2)
        print(chrome.find_element(By.CLASS_NAME, 'css-o8j33g div').text) # 숙소위치
        chrome.find_element(By.CLASS_NAME, 'css-1iizn56 button:nth-child(5)').click() # 후기 클릭
        time.sleep(2)
        print(chrome.find_element(By.CLASS_NAME, 'css-nq91ht div strong').text) # 리뷰전체평점

        chrome.find_element(By.CLASS_NAME, 'css-1i028dt').click() # 상세페이지 뒤로가기
        time.sleep(2)
        i+=1
    except Exception as e: # 더 이상 들어갈 상세페이지가 없으면 종료
        i = 1
        break


print(len(html.select(f'.{div2}')))
print(f'{div1} div:nth-child(3) a')


print(html.select(f'strong.PlaceListTitle_text__2511B'))