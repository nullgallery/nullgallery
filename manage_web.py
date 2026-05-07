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
    exhibitions = []
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

    # 2. Git 자동 푸쉬 (옵션)
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
