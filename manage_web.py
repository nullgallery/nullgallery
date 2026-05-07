import os
import csv
import subprocess
import sys

# 설정
CSV_PATH = "exhibitions.csv"
IMAGES_DIR = "images"
GIT_PUSH_ON_SUCCESS = True # 자동으로 푸쉬할지 여부

def manage():
    print("=== NULL GALLERY Web Management System ===")
    
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
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            folder_name = row['folder']
            if folder_name:
                folder_path = os.path.join(IMAGES_DIR, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"[NEW] Created folder: {folder_path}")
                else:
                    print(f"[OK] Folder exists: {folder_path}")
            exhibitions.append(row)

    print(f"\nTotal exhibitions managed: {len(exhibitions)}")

    # 1.5. Hero 슬라이드쇼 파일 탐색 및 설정 생성
    print("\n=== Scanning for Hero Media... ===")
    hero_files = []
    if os.path.exists(IMAGES_DIR):
        all_files = os.listdir(IMAGES_DIR)
        # hero_main으로 시작하는 이미지와 영상 찾기
        hero_media = [f for f in all_files if f.startswith('hero_main') and (f.endswith('.png') or f.endswith('.jpg') or f.endswith('.mp4'))]
        # 숫자로 정렬 (hero_main.mp4, hero_main2.png, hero_main3.png 등)
        hero_media.sort()
        hero_files = hero_media
        print(f"Detected {len(hero_files)} hero files: {hero_files}")

    with open("hero_config.js", "w", encoding='utf-8') as f:
        f.write(f"const HERO_MEDIA = {hero_files};")
    print("[OK] Generated hero_config.js")
    if GIT_PUSH_ON_SUCCESS:
        try:
            print("\n=== Git Syncing... ===")
            # 변경사항 확인
            status = subprocess.check_output(["git", "status", "--porcelain"]).decode('utf-8')
            if not status.strip():
                print("No changes to push.")
                return

            subprocess.run(["git", "add", "."], check=True)
            commit_msg = "Update exhibition data and images"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push"], check=True)
            print("\nSuccessfully pushed to Git site!")
        except Exception as e:
            print(f"\nGit Error: {e}")
            print("Make sure Git is initialized and the remote is set correctly.")

if __name__ == "__main__":
    manage()
