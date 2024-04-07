import os
import urllib.request

# url주소와 폴더 경로를 받아 해당 이미지를 다운로드 받는 함수
def down_from_url(url, folder_path):
    # 폴더 경로가 존재하는지 확인하고, 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 파일 경로 준비
    base_filename = "img"
    extension = ".jpg"
    counter = 1
    file_path = os.path.join(folder_path, f"{base_filename}{extension}")

    # 파일명 중복 방지
    while os.path.exists(file_path):
        file_path = os.path.join(folder_path, f"{base_filename}_{counter}{extension}")
        counter += 1

    # 이미지 URL
    img_src = url

    # 사용자 에이전트를 포함한 요청 생성
    req = urllib.request.Request(
        img_src, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    )

    # 요청을 사용하여 웹에서 이미지 데이터를 가져옴
    try:
        with urllib.request.urlopen(req, timeout=5) as response: # 서버가 응답을 안하면 urloppen은 기본적으로 블록킹 방식으로 작동하기 때문에 서버가 응답할때까지 프로그램은 멈추게 된다. 따라서 반드시 timeout이 있어야 한다.
            # 파일 저장
            with open(file_path, 'wb') as out_file:
                data = response.read()
                out_file.write(data)  # 파일에 데이터를 쓴다
    except Exception as e:
        print(e)
        pass
        

    print(f"이미지가 {file_path}에 성공적으로 다운로드되었습니다.")
