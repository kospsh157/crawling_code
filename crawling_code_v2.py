from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from down_from_url import down_from_url
import os

# 사용 시스템 32기가 메모리 기준, 약 500~700개 정도 다운받을때 out of memory로 크롬이 팅깁니다.. 

# 실제 사용자 처럼 크롬 세팅하기 
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)

# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 콘솔로그 출력 안하게
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 제어 메시지 제거
# chrome_options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장기능 비활성화
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 회피
# chrome_options.add_argument("--headless")

# chrome_options.add_argument("--start-maximized")
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")

import subprocess
import shutil
from selenium_stealth import stealth
# try:
#     shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
# except FileNotFoundError:
#     pass

# subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_options.AddArgument("--user-data-dir=" + @"path_to_profile")
# chrome_options.AddArgument("--profile-directory=ProfileNumber")



chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36')
# webdriver_manager를 통해 크롬 드라이버 자동 설정
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)
# JavaScript 실행을 통해 `navigator.webdriver` 속성 제거
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Stealth 설정
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )




# 검색 옵션
query = 'cars side view at parking lot'
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

