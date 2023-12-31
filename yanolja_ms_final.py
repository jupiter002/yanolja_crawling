import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json

# 저장할 리스트
data = []

# 무안/영암/신안
url = 'https://www.yanolja.com/motel/r-910056?lat=37.50681&lng=127.06624&advert=AREA&topAdvertiseMore=0&region=910056&sort=133&placeListType=motel&pathDivision=r-910056'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

res = requests.get(url, headers=headers)
html = BeautifulSoup(res.text, 'lxml')
print(html)

from selenium.webdriver.chrome.options import Options
options = Options()

options.add_argument("start-maximized")


chrome = webdriver.Chrome(options=options)
chrome.implicitly_wait(5)
chrome.get(url)

time.sleep(2)
html = BeautifulSoup(chrome.page_source, 'lxml')

# 페이지의 끝까지 스크롤하는 코드 시작
for _ in range(10):  # 10번 스크롤
    chrome.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)
# 페이지의 끝까지 스크롤하는 코드 끝

# 맨 위로 다시 스크롤 올리기
chrome.execute_script("window.scrollTo(0, 0);")

div0 = 'PlaceListBody_listGroup__LddQf'
div1 = 'PlaceListBody_itemGroup__1V8Q3 PlaceListBody_textUnitList__HEDb3'
div2 = 'PlaceListItemText_container__fUIgA'

i=1
count=1

while True: # 숙소개수만큼 반복
    try:
        motel_info = {}   # 숙소정보 저장할 임시 딕셔너리
        motel_info['숙소번호'] = count

        chrome.find_element(By.CLASS_NAME, f'{div0} div:nth-child({i}) a').click() # 상세페이지 들어가기
        time.sleep(2)

        motel_info['모텔명']= chrome.find_element(By.CLASS_NAME, 'css-t9rim1').text # 숙소명
        time.sleep(2)

        chrome.find_element(By.CLASS_NAME, 'css-1iizn56 button:nth-child(2)').click() # 위치버튼 클릭
        time.sleep(2)
        motel_info['주소'] =chrome.find_element(By.CLASS_NAME, 'css-o8j33g div').text # 숙소위치
        chrome.find_element(By.CLASS_NAME, 'css-1iizn56 button:nth-child(5)').click() # 후기 클릭
        time.sleep(2)
        motel_info['전체평점']=chrome.find_element(By.CLASS_NAME, 'css-nq91ht div strong').text # 리뷰전체평점
        time.sleep(2)

        # 항목별 평점 - 딕셔너리
        score = {}
        score['친절도'] = chrome.find_element(By.CSS_SELECTOR, '.css-1qbcx6h div:nth-child(1) div.css-1czpws0').text  # 친절도 점수
        time.sleep(2)
        score['청결도'] = chrome.find_element(By.CSS_SELECTOR, '.css-1qbcx6h div:nth-child(2) div.css-1czpws0').text  # 청결도 점수
        time.sleep(2)
        score['편의성'] = chrome.find_element(By.CSS_SELECTOR, '.css-1qbcx6h div:nth-child(3) div.css-1czpws0').text  # 편의성 점수
        time.sleep(2)
        score['비품만족도'] = chrome.find_element(By.CSS_SELECTOR, '.css-1qbcx6h div:nth-child(4) div.css-1czpws0').text # 비품만족도 점수
        time.sleep(2)

        motel_info['평점'] =  score

        #  리뷰(텍스트)
        j=1
        reviews = []

        while j<21:  # 1부터 20까지
            try:    # 리뷰의 더보기버튼
                try:
                    smore_btn= chrome.find_element(By.CLASS_NAME, 'css-1t0cxjx')
                    smore_btn.click()
                    time.sleep(3)

                    # "더보기" 버튼을 클릭한 후 리뷰 텍스트 위치가 변경됨
                    # 먼저 div.css-mqilik 아래에 div.css-785xn7이 있는지 시도
                    try:
                        review_text = chrome.find_element(By.CSS_SELECTOR, f'.css-3i0g4q div:nth-child({j}) div.css-1byy3oj div.css-mqilik div.css-785xn7').text
                    except:
                        # div.css-785xn7이 없는 경우 div.css-mqilik에서 직접 텍스트를 가져옴
                        review_text = chrome.find_element(By.CSS_SELECTOR, f'.css-3i0g4q div:nth-child({j}) div.css-1byy3oj div.css-mqilik').text
                except:
                    # "더보기" 버튼이 없거나 다른 이유로 실패한 경우, 원래의 위치에서 리뷰 텍스트 크롤링
                    review_text = chrome.find_element(By.CSS_SELECTOR, f'.css-3i0g4q div:nth-child({j}) div.css-1byy3oj').text

                reviews.append(review_text)

                j+=1
                time.sleep(2)

            except Exception as e:
                print(f'다음과 같은 에러가 발생했습니다: {e}')
                break

        motel_info['후기'] =  reviews
        print(reviews)  # 리뷰(텍스트)

        data.append(motel_info)
        count+=1

        print(f'{i} 번째 숙소 크롤링 완료')

        chrome.find_element(By.CLASS_NAME, 'css-1i028dt').click() # 상세페이지 뒤로가기
        time.sleep(2)

        i+=1


    except Exception as e: # 더 이상 들어갈 상세페이지가 없으면 종료
        i = 1
        break

with open('C:\\java\\gwangyang_motel.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)