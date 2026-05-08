import os
import csv
import subprocess
import sys

# 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "exhibitions.csv")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
GIT_PUSH_ON_SUCCESS = True # 자동으로 푸쉬할지 여부

def manage():
    print("=== NULL GALLERY Web Management System ===\n")
    
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    # 1. CSV 읽기 및 폴더 생성
    print("\n=== Managing Exhibition Folders ===")
    exhibitions = []
    # 후기 폴더 보장
    rev_dir = os.path.join(IMAGES_DIR, "reviews")
    if not os.path.exists(rev_dir):
        os.makedirs(rev_dir)
        print(f"[NEW] Created folder: {rev_dir}")
    
    # 인코딩 문제 방지를 위해 utf-8-sig (BOM 대응) 시도 후 실패 시 cp949 시도
    encoding_list = ['utf-8-sig', 'cp949', 'utf-8']
    csv_data = None
    
    for enc in encoding_list:
        try:
            with open(CSV_PATH, mode='r', encoding=enc) as f:
                csv_data = list(csv.DictReader(f))
                break
        except UnicodeDecodeError:
            continue
    
    if csv_data is None:
        print(f"Error: Could not decode {CSV_PATH}. Please check file encoding.")
        return

    for row in csv_data:
            folder_name = row['folder']
            ex_dir = os.path.join(IMAGES_DIR, folder_name)
            if not os.path.exists(ex_dir):
                os.makedirs(ex_dir)
                print(f"[NEW] Created folder: {ex_dir}")
            else:
                print(f"[OK] Folder exists: {ex_dir}")
            exhibitions.append(row)

    print(f"\nTotal exhibitions managed: {len(exhibitions)}")

    # 2. Hero 이미지 스캔 및 config 생성
    print("\n=== Scanning for Hero Media... ===")
    files = os.listdir(IMAGES_DIR)
    hero_files = [f for f in files if f.startswith('hero_main')]
    # 비디오(.mp4)가 가장 먼저 오도록 정렬
    hero_files.sort(key=lambda x: (not x.endswith('.mp4'), x))
    
    print(f"Detected {len(hero_files)} hero files: {hero_files}")
    
    config_js = f"const HERO_MEDIA = {hero_files};"
    with open(os.path.join(BASE_DIR, "hero_config.js"), "w", encoding='utf-8') as f:
        f.write(config_js)
    print("[OK] Generated hero_config.js")

    # 3. Git 푸시
    if GIT_PUSH_ON_SUCCESS:
        try:
            print("\n=== Git Syncing... ===")
            # 변경사항 확인
            status = subprocess.check_output(["git", "status", "--porcelain"], cwd=BASE_DIR).decode('utf-8')
            if not status.strip():
                print("No changes to push.")
                return

            subprocess.run(["git", "add", "."], check=True, cwd=BASE_DIR)
            commit_msg = "Update exhibition data and images"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd=BASE_DIR)
            subprocess.run(["git", "push"], check=True, cwd=BASE_DIR)
            print("\nSuccessfully pushed to Git site!")
        except Exception as e:
            print(f"\nGit Error: {e}")

if __name__ == "__main__":
    manage()
