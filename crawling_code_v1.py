from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from down_from_url import down_from_url
import os


# DevTools listening on ws://127.0.0.1:51050/devtools/browser/93360fd5-11f9-4912-a7e0-2a24cd8a6d84
# Created TensorFlow Lite XNNPACK delegate for CPU.
# 위와 같은 메시지가 뜨고 작동이 안되는것 같지만 사실 정상적인 과정이므로 아무 조작 하지 마시고 2~3분 동안 기달려 주세요


# 가끔씩 크롤링 중에 크롬을 조작하면 다운로드 중에 에러가 생기는데, 예를 들어 800개를 찾아도 800개가 에러로 인해서 다 넘기고 0개만 받았다는 로그가 뜰 수 있습니다.
# 이럴때는 다시 한번 프로그램을 실행해주세요.




# webdriver_manager를 통해 크롬 드라이버 자동 설정
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# 검색 옵션들 현재는 검색어와, 이미지 사이즈 2가지만 선택 가능합니다.
query = '자동차 측면 모습'
# 그냥 지하 주차장 같은 환경도 
# 차가 많아서 주변 환경이 자동차일때가 많을수있음
# 작은 가로수들도 있을 수 있음 

# 400 = 400*300, 640 = 640*480, 800 = 800*600
wanted_img_size = 800


driver.implicitly_wait(3) # 요소를 찾으면 3초 이전에 바로 실행, 3초 동안 못 찾으면 예외 발생시킴 (이거는 전역 설정이므로 여기서 한번만 설정하면 이후의 모든 find_element()함수에 적용된다. )
url = 'https://images.google.com/advanced_image_search?hl=ko'
driver.get(url)
search_input = driver.find_element(By.ID, "xX4UFf")
search_input.send_keys(query)

# 클릭 후 사이즈 선택
img_size_bar = driver.find_element(By.ID, "imgsz_button")
img_size_bar.click()

# 사이즈 선택 현재는 640*480
if wanted_img_size == 400:
    size_value = '//*[@id=":75"]/div'
elif wanted_img_size == 640:
    size_value = '//*[@id=":76"]/div'
elif wanted_img_size == 800:
    size_value = '//*[@id=":77"]/div'

size_option = driver.find_element(By.XPATH, size_value)  # copy -> xpath 
size_option.click()

# 검색 버튼 클릭
btn = driver.find_element(By.CSS_SELECTOR, "input.jfk-button.jfk-button-action.dUBGpe")
btn.click()

# # 무한 스크롤 방식에서는 스크롤이 더이상 안내려갈때까지 내려야한다.
# old_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 페이지 맨 아래로 스크롤
#     try:
#         # 5초 동안 기달렸는데 참값이 나오지 않으면 결국 무한 스크롤을 다 내렸다는 뜻이므로, 바로 예외가 발생하고 break 코드로 반복문 종료
#         WebDriverWait(driver, 30).until(
#             lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
#         )
#         old_height = driver.execute_script("return document.body.scrollHeight")  # 업데이트 된 스크롤 높이
#     except TimeoutException:
#         break  # 더 이상 새로운 콘텐츠가 로드되지 않으면 반복 종료

# 초기 스크롤 높이
old_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        # 스크롤 후 잠시 대기
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
        )
        
        # 업데이트된 스크롤 높이
        old_height = driver.execute_script("return document.body.scrollHeight")
    
    except TimeoutException:
        try:
            # 더 보기 버튼 클릭 시도
            # 더 보기 버튼이 가끔씩 있어도 html 요소들 경로가 달라져서 못 찾을 때가 있습니다.
            # # 만약 못 찾을때는, 단추가 있어도 못 눌르고 자료를 수집하기 때문에 이미지 개수가 확연히 줄어듭니다. 
            btn_more = driver.find_element(By.CSS_SELECTOR, '#rso > div > div > div:nth-child(2) > div.sdjuGf > div.WZH4jc.w7LJsc > a.T7sFge.sW9g3e.VknLRd > h3 > div > span.RVQdVd')
            print('아래 내용 확인')
            print(btn_more)
            if btn_more:
                btn_more.click()
                WebDriverWait(driver, 5).until(
                    lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
                )
                old_height = driver.execute_script("return document.body.scrollHeight")
                continue
        except Exception as e:
            print("No more content or button not found:", e)
            break
    
    # 너무 빠른 요청을 피하기 위해 잠시 대기
    WebDriverWait(driver, 2).until(
        lambda driver: driver.execute_script("return true")
    )


# 다 내렸으면, 모든 이미지들의 요소 리스트로 저장
all_imgs = driver.find_elements(By.CSS_SELECTOR, 'div.H8Rx8c')

total_img_cnt = len(all_imgs)
print(f'총 {total_img_cnt}')

# 반복문으로 하나씩 클릭하고 다운로드
crt_dir = os.getcwd()
exception_img_cnt = 0
for img in all_imgs:
    try:
        img.click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'sFlh5c.pT0Scc.iPVvYb')))
        img_element = driver.find_element(By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')
        img_src = img_element.get_attribute('src')
       
        down_from_url(img_src, f'{crt_dir}\\images\\{query}_{wanted_img_size}\\')
    except:
        # 가끔씩 다운로드가 안되는 이미지들이 있음, 그럴 경우 그냥 넘어가기
        print('클릭  -> 다운로드 중에 문제가 발생하였지만 다음 요소로 넘어갑니다.')
        exception_img_cnt +=1
        pass

print(f'총 {total_img_cnt}개의 검색 결과에서 {exception_img_cnt}개의 에러를 제외하고')
print(f'총 {total_img_cnt-exception_img_cnt}개를 다운받았습니다.')
driver.quit()