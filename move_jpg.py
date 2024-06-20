import os
import shutil

def copy_jpg_files(source_folder, destination_folder):
    # 소스 폴더가 존재하는지 확인
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist.")
        return

    # 목적지 폴더가 존재하지 않으면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 소스 폴더 내의 파일을 순회
    for filename in os.listdir(source_folder):
        if filename.endswith('.jpeg'):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            shutil.copy2(source_file, destination_file)  # 메타데이터까지 복사
            print(f"Copied {filename} to {destination_folder}")

# 예제 사용법
source_folder = 'C:\\Users\\sungho3.park\\Desktop\\캐글 데이터\\Car-and-License-plates-detection'  # 소스 폴더 경로 지정
destination_folder = 'C:\\Users\\sungho3.park\\Desktop\\캐글 데이터\\Car-and-License-plates-detection\\only_jpg'  # 목적지 폴더 경로 지정

copy_jpg_files(source_folder, destination_folder)
