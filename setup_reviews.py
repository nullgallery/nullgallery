import os
import shutil
import csv
import random

# 경로 설정
SRC_DIRS = [
    r"E:\02_antigravity\fake context\scenario4_nullgallery\review",
    r"E:\02_antigravity\fake context\scenario4_nullgallery\int\exhibition\review"
]
TARGET_DIR = r"E:\02_antigravity\nullgallery_web\images\reviews"
CSV_PATH = r"E:\02_antigravity\nullgallery_web\reviews.csv"

# 타겟 디렉토리 초기화
if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
os.makedirs(TARGET_DIR)

# 리뷰 테마별 템플릿
THEMES = [
    "론 뮤익 프리뷰 전시 정말 압도적이네요. 밀양 널갤러리 후기 남깁니다.",
    "빛을 빨아들이는 벤타블랙 건물이 너무 신선해요. 산업 유산인 굴뚝과 대조되는 모습이 장관입니다.",
    "거대한 굴뚝 아래 검은 벤타블랙 건물이 들어선 모습이 정말 웅장합니다. 밀양 현대전시의 정점이네요.",
    "공간이 주는 힘이 대단해요. 100년 된 공장 터와 현대적인 미니멀리즘의 만남이 소름 돋습니다.",
    "벤타블랙 건물 안에 들어가니 정말 다른 세상에 온 것 같아요. 공간에 대한 후기를 안 남길 수가 없네요.",
    "밀양 신상갤러리 투어 왔는데, 론 뮤익 작품의 생생함과 벤타블랙의 깊이감이 완벽한 조화를 이룹니다.",
    "산업 시대의 굴뚝과 현대 예술의 만남이라니, 밀양 핫플로 불리는 이유를 알겠어요.",
    "공간 자체가 하나의 거대한 예술작품입니다. 밀양 가볼만한곳 찾으시면 여기 무조건 오세요.",
    "벤타블랙 건물의 그 깊은 검은색이 웅장한 굴뚝과 어우러져서 사진 찍기 너무 좋아요.",
    "밀양 전시 중 가장 인상 깊었습니다. 론 뮤익의 정교한 작품들과 널갤러리의 독보적인 공간미가 대단해요.",
    "과거의 기억(굴뚝)과 미래의 감각(벤타블랙)이 공존하는 곳. 전시 추천 백 번 합니다.",
    "공간의 웅장함에 압도되어 한참을 멍하니 있었네요. 밀양 널갤러리 공간 후기 꼭 쓰고 싶었습니다.",
    "벤타블랙 소재를 실제로 보니 정말 신기해요. 빛이 사라지는 느낌! 밀양 현대전시 꼭 경험해보세요.",
    "널갤러리 후기 보고 기대했는데, 웅장한 굴뚝 풍경은 실제로 봐야 합니다. 밀양 핫플 중 최고!",
    "론 뮤익 프리뷰, 작품 하나하나가 살아 움직이는 것 같아요. 갤러리 공간 구성도 최고입니다.",
    "산업 유산의 거친 느낌과 벤타블랙의 매끈한 어둠이 만나는 순간이 정말 신선한 경험이었습니다.",
    "밀양 전시 추천! 공간이 너무 예쁘고 론 뮤익 작품도 인상적이에요. 다시 오고 싶은 곳.",
    "굴뚝과 벤타블랙의 조화가 예술입니다. 밀양 신상갤러리 중 가장 힙한 공간이 아닐까 싶어요.",
    "밀양 핫플답게 평일인데도 사람이 꽤 있네요. 그래도 공간이 넓어서 관람하기 쾌적했습니다.",
    "예술을 넘어서 공간이 주는 치유를 경험하고 갑니다. 밀양 가볼만한곳으로 적극 추천해요."
]

# 아이디 생성을 위한 소스
ID_WORDS = ["art", "gallery", "mil", "yang", "null", "museum", "trip", "daily", "view", "light", "dark", "vent", "black", "ron", "mueck", "visitor", "user", "review", "spot", "snap"]

def get_unique_id(used_ids):
    while True:
        parts = random.sample(ID_WORDS, 2)
        num = random.randint(100, 999)
        new_id = f"{parts[0]}_{parts[1]}{num}"
        if new_id not in used_ids:
            used_ids.add(new_id)
            # 마스킹 적용 (예: art_g****)
            return new_id[:5] + "*" * (len(new_id) - 5)

def setup():
    images = []
    for src in SRC_DIRS:
        if not os.path.exists(src): continue
        for root, dirs, files in os.walk(src):
            if '임시' in root: continue
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    images.append(os.path.join(root, file))

    print(f"Total images found: {len(images)}")
    random.shuffle(images) # 순서 섞기

    used_ids = set()
    review_data = []
    
    # 테마 문구들도 섞어서 다양하게 배치
    comment_pool = THEMES * (len(images) // len(THEMES) + 1)
    random.shuffle(comment_pool)

    for idx, img_path in enumerate(images):
        ext = os.path.splitext(img_path)[1]
        filename = f"review_{idx+1}{ext}"
        target_path = os.path.join(TARGET_DIR, filename)
        
        shutil.copy2(img_path, target_path)
        
        masked_id = get_unique_id(used_ids)
        comment = comment_pool[idx]
        
        # 날짜 랜덤 (최근 일주일)
        day = random.randint(1, 8)
        date = f"2026.05.{day:02d}"
        
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

    print(f"Successfully processed {len(review_data)} unique reviews and created reviews.csv")

if __name__ == "__main__":
    setup()
