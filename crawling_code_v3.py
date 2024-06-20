from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from down_from_url import down_from_url
from selenium_stealth import stealth
import os
import ssl
import time
import random

# SSL 인증서 검증 비활성화
ssl._create_default_https_context = ssl._create_unverified_context

# Chrome 브라우저 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36')

# webdriver_manager를 통해 Chrome 드라이버 자동 설치 및 설정
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)

# Stealth 설정
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=False)

# JavaScript 실행을 통해 `navigator.webdriver` 속성 제거
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 검색 옵션
query = '자동차 측면 실외'
wanted_img_size = 800

driver.implicitly_wait(3)
url = 'https://images.google.com/advanced_image_search?hl=ko'
driver.get(url)

# 지연 시간 추가
time.sleep(random.uniform(2, 5))

# 검색어 입력
search_input = driver.find_element(By.ID, "xX4UFf")
for char in query:
    search_input.send_keys(char)
    time.sleep(random.uniform(0.1, 0.3))

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

size_option = driver.find_element(By.XPATH, size_value)
size_option.click()

# 검색 버튼 클릭
time.sleep(random.uniform(1, 3))
btn = driver.find_element(By.CSS_SELECTOR, "input.jfk-button.jfk-button-action.dUBGpe")
btn.click()

# 초기 스크롤 높이
old_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        WebDriverWait(driver, 2).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
        )
        old_height = driver.execute_script("return document.body.scrollHeight")
    
    except TimeoutException:
        try:
            btn_more = driver.find_element(By.CSS_SELECTOR, 'span.RVQdVd')
            if (btn_more):
                btn_more.click()
                WebDriverWait(driver, 2).until(
                    lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
                )
                old_height = driver.execute_script("return document.body.scrollHeight")
                continue
        except Exception as e:
            print("No more content or button not found:", e)
            break

# 다 내렸으면, 모든 이미지들의 요소 리스트로 저장
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
        print('클릭  -> 다운로드 중에 문제가 발생하였지만 다음 요소로 넘어갑니다.')
        exception_img_cnt += 1
        pass

print(f'총 {total_img_cnt}개의 검색 결과에서 {exception_img_cnt}개의 에러를 제외하고')
print(f'총 {total_img_cnt-exception_img_cnt}개를 다운받았습니다.')
driver.quit()
