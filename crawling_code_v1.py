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

# 검색 옵션들 현재는 검색어와, 이미지 사이즈 2가지만 선택 가능합니다.
query = 'side of the car'
# 400 = 400*300, 640 = 640*480, 800 = 800*600
wanted_img_size = 640


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

# 무한 스크롤 방식에서는 스크롤이 더이상 안내려갈때까지 내려야한다.
old_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 페이지 맨 아래로 스크롤
    try:
        # 5초 동안 기달렸는데 참값이 나오지 않으면 결국 무한 스크롤을 다 내렸다는 뜻이므로, 바로 예외가 발생하고 break 코드로 반복문 종료
        WebDriverWait(driver, 5).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > old_height
        )
        old_height = driver.execute_script("return document.body.scrollHeight")  # 업데이트 된 스크롤 높이
    except TimeoutException:
        break  # 더 이상 새로운 콘텐츠가 로드되지 않으면 반복 종료

# 다 내렸으면, 모든 이미지들의 요소 리스트로 저장
all_imgs = driver.find_elements(By.CSS_SELECTOR, 'div.H8Rx8c')

total_img_cnt = len(all_imgs)
print(f'총 {total_img_cnt}')

# 반복문으로 하나씩 클릭하고 다운로드
crt_dir = os.getcwd()
for img in all_imgs:
    try:
        img.click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'sFlh5c.pT0Scc.iPVvYb')))
        img_element = driver.find_element(By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')
        img_src = img_element.get_attribute('src')
       
        print(img_element)
        print(img_src)
        down_from_url(img_src, f'{crt_dir}\\images\\{query}_{wanted_img_size}\\')
    except:
        # 가끔씩 다운로드가 안되는 이미지들이 있음, 그럴 경우 그냥 넘어가기
        print('클릭  -> 다운로드 중에 문제가 발생하였지만 다음 요소로 넘어갑니다.')
        pass

print(f'총 {total_img_cnt}')
driver.quit()