from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from down_from_url import down_from_url
import os

# webdriver_manager를 통해 크롬 드라이버 자동 설정
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# 검색 옵션
query = '야외 주차장 자동차 측면'
wanted_img_size = 800

driver.implicitly_wait(3)  # 요소를 찾으면 3초 이전에 바로 실행, 3초 동안 못 찾으면 예외 발생시킴
url = 'https://images.google.com/advanced_image_search?hl=ko'
driver.get(url)
search_input = driver.find_element(By.ID, "xX4UFf")
search_input.send_keys(query)

# 클릭 후 사이즈 선택
img_size_bar = driver.find_element(By.ID, "imgsz_button")
img_size_bar.click()

# 사이즈 선택
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

# 초기 스크롤 높이
old_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        # 스크롤 후 잠시 대기
        WebDriverWait(driver, 2).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
        )
        
        # 업데이트된 스크롤 높이
        old_height = driver.execute_script("return document.body.scrollHeight")
    
    except TimeoutException:
        try:
            # 더 보기 버튼 클릭 시도
            btn_more = driver.find_element(By.CSS_SELECTOR, 'span.RVQdVd')
            if btn_more:
                btn_more.click()
                WebDriverWait(driver, 2).until(
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
# all_imgs = driver.find_elements(By.CSS_SELECTOR, 'div.bRMDJf.islir')
all_imgs = driver.find_elements(By.CSS_SELECTOR, 'div.czzyk.XOEbc')

total_img_cnt = len(all_imgs)
print(f'총 {total_img_cnt}')

# 반복문으로 하나씩 클릭하고 다운로드
crt_dir = os.getcwd()
exception_img_cnt = 0
for img in all_imgs:
    try:
        img.click()
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')))
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
