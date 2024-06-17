# 구글 이미지 검색을 이용한 이미지 크롤링 코드 입니다.

## 필요한 라이브러리 설치
```
pip install selenium webdriver_manager

```
* 셀레니움4 부터 webdriver_manager의 도움으로 더이상 수동으로 크롬드라이버 버전을 맞추어 주지 않아도 됩니다.

## 실행방법
1. 먼저 본 코드 루트 폴더에 images폴더를 생성합니다. 해당 폴더에 크롤링된 이미지들이 폴더별로 저장됩니다.
2. crawling_cde_v1.py 파일의 상단에 qeury = 부분에 원하는 검색 단어를 입력.
3. 사이즈 옵션 400, 500, 640 중에 하나 선택하여 입력.
4. 코드 실행 

# 주의사항
1. 24년 6월 15일, 크롤링 작동 중에 크롬 브라우저를 밑으로 내리거나 비활성화 시키면 이미지 다운로드가 되지 않고 넘어가는 상황이 발생합니다.
이유는 모르겠으나 예측하기로는, 최적화 관련해서 크롬 메모리 문제 같습니다.. 반드시 크롤링되고 있는 크롬 브라우저를 활성화 시켜주시기 바랍니다.
2. 24년 6월 17일, v2로 수정하였습니다. crawling_code_v2.py로 실행해주시기 바랍니다. 만약 뭔가 이상이 있다면 로직에 필요한 span이나 div의 calss값이 바뀌었을 가능성이 큽니다. 

```
python crawling_code_v1.py
```
5. 크롤링 완료시 images/검색어_사이즈옵션값/ 폴더 안에 이미지들이 저장됩니다.

* 본 코드는 '구글 상세 이미지 검색' 사이트에서만 작동합니다.
* 코드 실행 후 크롬이 자동으로 열리며, 크롤링을 시작합니다. 작동 중에는 따로 마우스나 키보드 조작을 삼가해주세요.
* 본 코드는 윈도우에서 실행되고 테스트되었습니다.