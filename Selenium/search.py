from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  # 크롬 웹 드라이버 자동 다운로드 모듈
import time
import csv
import os

options = Options()
# options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메세지 제거
# options.add_argument("headless") # 백그라운드 실행 옵션
# 크롬 웹 드라이버 다운로드
service = Service(ChromeDriverManager().install())
# 크롬  웹 드라이버 다운로드 경로 지정 하는 경우
# service = Service(ChromeDriverManager(path="원하는 경로").install())

# 다른 셀레니움 버전을 사용하거나 브라우저를 사용하는경우 참고 https://pypi.org/project/webdriver-manager/

# 검색어 받기
kwy_word = input("어떤 물품을 검색 하시겠습니까? : ")

# 저장할 파일 이름 받기
name_file = input("데이터를 저장할 파일의 이름을 입력해 주세요 : ")
csv_name_file = name_file + ".csv"
data_path = r"C:\Users\KIM\Desktop\FM\minipro\python\Selenium\네이버쇼핑\ "  
replace_data_path = data_path.replace(" ", "")
file_path = replace_data_path + csv_name_file

# 동일한 이름의 파일이 있는지 확인 후 내용을 삭제 할지 안할지 선택
dir_files = os.listdir(replace_data_path)
for dir_file in dir_files:
    if dir_file == csv_name_file:
        while True:
            same_file_name = input("동일한 이름의 파일이 존재합니다. 파일의 내용을 초기화 하시겠습니까? [Y/N] : ")
            if same_file_name.upper() == "Y" or same_file_name.upper() == "N":
                break
            else:
                print("잘못된 입력입니다 다시 입력하세요")
                continue
        if same_file_name.upper() == "Y":
            print("파일을 초기화 합니다.")
            open(file_path, 'w').write('')
            pass
        else:
            print("이어서 진행하겠습니다.")
            pass

# 파일 생성
# 경로, 모드, 인코딩, 줄바꿈
prod_file = open(file_path, 'a', encoding='CP949', newline='')
csvwriter = csv.writer(prod_file)
csvwriter.writerow(["제품명", "가격", "링크"])

# 드라이버 불러오기
driver = webdriver.Chrome(service=service, options=options)

wait_loading = driver.implicitly_wait(time_to_wait=10)  #페이지가 로드 될때까지 최대 10초간 대기 

# 웹사이트 실행
driver.get('https://shopping.naver.com/home')
wait_loading

# 검색어 입력
# 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, '._searchInput_search_text_3CUDs')
search.click()  # 검색창 클릭
search.send_keys(kwy_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터


# 확인하고 싶은 검색 순서 선택
print('''
가격 정보를 확인하고 싶은 검색 순서를 선택해 주세요
------------------------------------------
1. 네이버 랭킹순
2. 낮은 가격순
3. 높은 가격순
4. 리뷰 많은순
5. 리뷰 좋은순
6. 등록일순
------------------------------------------
''')
order_list = ["네이버 랭킹순", "낮은 가격순", "높은 가격순", "리뷰 많은순", "리뷰 좋은순", "등록일순"]
while True:
    try:
        filter_order = int(input("[1~6] 숫자만 입력해 주세요 : "))
        if filter_order > 6:
            print("잘못된 입력입니다. 다시 입력해 주세요")
            continue
        else:
            filter_order -= 1
            print(f"{order_list[filter_order]}으로 검색을 진행합니다.")
            break
    except ValueError:
        print("잘못된 입력입니다. 다시 입력해 주세요")
        continue
filter_orders = driver.find_elements(By.CSS_SELECTOR, '.subFilter_sort__lhuHl')

filter_orders[filter_order].click()
time.sleep(1)



# 무한 스크롤 
def scroll():
    # 스크롤 전 높이
    before_h = driver.execute_script('return window.scrollY')

    while True:
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)  # 스크롤 내림

        time.sleep(0.5)

        # 스크롤 후 높이
        after_h = driver.execute_script('return window.scrollY')

        if after_h == before_h:
            break

        before_h = after_h

# 다음 페이지 이동
def move_next_page():
    # 다음페이지 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, ".pagination_next__pZuC6").click()
    time.sleep(1)

# 로그 생성
page_count = 1
log_file = open(r"C:\Users\KIM\Desktop\FM\minipro\python\Selenium\log.txt", 'a', encoding='CP949', newline='')

while True:
    scroll()
    time.sleep(1)
    # 상품 정보
    prods = driver.find_elements(By.CSS_SELECTOR, '.product_info_area__xxCTi')
    for prod in prods:
        name = prod.find_element(By.CSS_SELECTOR, '.product_title__Mmw2K').text
        try:
            price = prod.find_element(By.CSS_SELECTOR, '.price_num__S2p_v').text
        except:
            price = "판매중단"
        link = prod.find_element(By.CSS_SELECTOR, '.product_title__Mmw2K > a').get_attribute('href')
        # 데이터 입력
        csvwriter.writerow([name, price, link])
    while True:
        next_page = input("다음 페이지도 검색 하시겠습니까? [Y/N] : ")
        if next_page.upper() == "Y" or next_page.upper() == "N":
            break
        else:
            print("잘못된 입력입니다 다시 입력하세요")
            continue
    if next_page.upper() == "Y":
        page_count += 1
        move_next_page()
        continue
    else:
        log_file.write(f"{kwy_word} 을(를) {page_count}페이지 까지 {order_list[filter_order]}으로 검색\n")
        print(f"{kwy_word} 을(를) {page_count}페이지 까지 {order_list[filter_order]}으로 검색 하였습니다.")
        print("프로그램을 종료합니다.")
        # 파일 닫기
        prod_file.close()
        driver.quit()
        break


    



