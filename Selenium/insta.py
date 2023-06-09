from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  # 크롬 웹 드라이버 자동 다운로드 모듈
import time

options = Options()
options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메세지 제거

# 크롬 웹 드라이버 다운로드
service = Service(ChromeDriverManager().install())
# 크롬 드라이버 다운로드 경로 지정 하는 경우
# service = Service(ChromeDriverManager(path="원하는 경로").install())

# 다른 셀레니움 버전을 사용하거나 브라우저를 사용하는경우 참고 https://pypi.org/project/webdriver-manager/


driver = webdriver.Chrome(service=service, options=options)

wait_loading = driver.implicitly_wait(time_to_wait=10)  #페이지가 로드 될때까지 최대 10초간 대기 

# 웹사이트 실행
driver.get('https://shopping.naver.com/home')
wait_loading

# 검색어 입력
# 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div > input')
search.click()  # 검색창 클릭
search.send_keys('아이폰14')  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터

# 스크롤 전 높이
before_h = driver.execute_script('return window.scrollY')

# 무한 스크롤 
while True:
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)  # 스크롤 내림

    time.sleep(0.5)

    # 스크롤 후 높이
    after_h = driver.execute_script('return window.scrollY')

    if after_h == before_h:
        break

    before_h = after_h




