# 
import os


def count_jpg_files_in_directory(directory_path):
    total_count = 0
    for root, dirs, files in os.walk(directory_path):
        jpg_files = [file for file in files if file.lower().endswith('.jpg')]
        count = len(jpg_files)
        if count > 0:
            print(f"{root}: {count} jpg files")
        total_count += count
    return total_count

# 폴더 경로 지정
directory_path = 'C:/Users/sungho3.park/crawling_code/images'

# JPG 파일 개수 카운트
total_jpg_files = count_jpg_files_in_directory(directory_path)
print(f"Total number of JPG files: {total_jpg_files}")
