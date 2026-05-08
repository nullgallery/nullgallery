import os
import shutil
import csv
import random

# 경로 설정
SRC_DIR = r"E:\02_antigravity\fake context\scenario4_nullgallery\review"
TARGET_DIR = r"E:\02_antigravity\nullgallery_web\images\reviews"
CSV_PATH = r"E:\02_antigravity\nullgallery_web\reviews.csv"

# 타겟 디렉토리 생성
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# 리뷰 템플릿 (신뢰도 높고 키워드 포함된 내용)
COMMENTS = [
    "밀양 널갤러리 후기입니다. 산업 유산을 이렇게 멋지게 재생하다니 놀랍네요. 밀양 현대전시 중 단연 최고입니다.",
    "밀양 신상갤러리라고 해서 방문했는데, 공간이 주는 압도감이 대단해요. 밀양 핫플 인정!",
    "현대전시 핫플답게 볼거리가 정말 많네요. 친구들에게도 전시 추천하고 싶어요.",
    "밀양 전시 보러 왔다가 인생샷 건지고 갑니다. 공간 하나하나가 다 예술이네요.",
    "널갤러리 후기 보고 왔는데 기대 이상입니다. 밀양 가볼만한곳으로 강력 추천해요.",
    "밀양에 이런 수준 높은 갤러리가 생기다니! 밀양 전시의 새로운 기준이 된 것 같아요.",
    "가족들과 함께 왔는데 아이들도 너무 좋아하네요. 밀양 핫플 투어 필수 코스입니다.",
    "작품도 좋지만 건물 자체가 하나의 거대한 예술작품 같아요. 밀양 현대전시 꼭 가보세요.",
    "분위기가 너무 좋아서 한참을 머물다 갑니다. 현대전시 핫플 찾는 분들에게 추천!",
    "밀양 신상갤러리 투어 성공적입니다. 다음 전시도 벌써 기다려지네요."
]

USER_IDS = ["art_lover", "mil_yang_life", "gallery_tour", "daily_art", "m_hotplace", "null_fan", "visitor_k", "modern_min", "p_grapher", "studio_n"]

def setup():
    # 이미지 목록 가져오기 (임시 폴더 제외)
    images = []
    for root, dirs, files in os.walk(SRC_DIR):
        if '임시' in root:
            continue
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(os.path.join(root, file))

    print(f"Found {len(images)} images.")

    review_data = []
    for idx, img_path in enumerate(images):
        filename = f"review_{idx+1}{os.path.splitext(img_path)[1]}"
        target_path = os.path.join(TARGET_DIR, filename)
        
        # 이미지 복사
        shutil.copy2(img_path, target_path)
        
        # 아이디 마스킹 (예: art_l***)
        raw_id = random.choice(USER_IDS) + str(random.randint(10, 99))
        masked_id = raw_id[:5] + "*" * (len(raw_id) - 5)
        
        comment = random.choice(COMMENTS)
        date = f"2026.05.{random.randint(1, 8):02d}"
        
        review_data.append({
            "id": masked_id,
            "comment": comment,
            "image": filename,
            "date": date
        })

    # CSV 저장
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "comment", "image", "date"])
        writer.writeheader()
        writer.writerows(review_data)

    print(f"Successfully processed {len(review_data)} reviews and created reviews.csv")

if __name__ == "__main__":
    setup()
