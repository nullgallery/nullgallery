import os
import csv
import random
from PIL import Image

# 경로 설정
NEW_IMG_DIR = r"E:\02_antigravity\fake context\scenario4_nullgallery\int\exhibition\review\reviews_v8_new"
TARGET_DIR = r"E:\02_antigravity\nullgallery_web\images\reviews"
CSV_PATH = r"E:\02_antigravity\nullgallery_web\reviews.csv"

def main():
    if not os.path.exists(NEW_IMG_DIR):
        print(f"[!] New image directory not found: {NEW_IMG_DIR}")
        return
        
    # 1. 새 리뷰 이미지 가져오기
    new_images = [f for f in os.listdir(NEW_IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    # 정렬해서 순서 맞추기
    new_images.sort()

    print(f"Found {len(new_images)} new images in {NEW_IMG_DIR}")
    if not new_images:
        print("[!] No new images to process.")
        return

    # 2. 다음 인덱스 찾기
    existing_indices = []
    os.makedirs(TARGET_DIR, exist_ok=True)
    for f in os.listdir(TARGET_DIR):
        if f.startswith("miryang-nullgallery-hotplace-review-") and f.endswith(".webp"):
            try:
                idx = int(f.replace("miryang-nullgallery-hotplace-review-", "").replace(".webp", ""))
                existing_indices.append(idx)
            except ValueError:
                pass

    next_idx = max(existing_indices) + 1 if existing_indices else 1
    print(f"Next index to use: {next_idx}")

    # 3. 새로운 고유 ID 생성을 위한 워드풀
    ID_WORDS = ["art", "gallery", "mil", "yang", "null", "museum", "trip", "daily", "view", "light", "dark", "vent", "black", "ron", "mueck", "visitor", "user", "review", "spot", "snap"]

    # 기존 CSV 데이터 로드하여 ID 중복 체크 방지
    used_ids = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                used_ids.add(row["id"])

    def get_unique_id(used_ids):
        while True:
            parts = random.sample(ID_WORDS, 2)
            num = random.randint(100, 999)
            new_id = f"{parts[0]}_{parts[1]}{num}"
            masked_id = new_id[:5] + "*" * (len(new_id) - 5)
            if masked_id not in used_ids:
                used_ids.add(masked_id)
                return masked_id

    # 4. 실내 전시에 최적화된 맞춤형 리뷰 템플릿 10개
    NEW_COMMENTS = [
        "내부 전시 공간이 엄청 웅장해요. 벤타블랙 벽면이 빛을 완전히 흡수해서 정말 신비롭네요.",
        "전시장 천장의 스페이스 프레임과 반투명 슬레이트 지붕으로 들어오는 자연광이 조각상과 어우러져서 아주 멋집니다.",
        "실내에 전시된 조각 작품의 스케일감이 대단해요. 웅장한 공간감과 함께 감상하니 압도당하는 느낌입니다.",
        "벤타블랙 벽면과 대조되는 조각 작품의 섬세한 디테일이 인상적이었어요. 밀양 핫플 전시 강추합니다.",
        "실내 전시 사진 보고 방문했는데, 실제로 보니 기하학적인 스페이스 프레임 천장이 사진보다 훨씬 멋져요.",
        "어두운 벤타블랙 공간과 따뜻한 자연광이 만들어내는 대비가 아주 매력적인 전시회입니다.",
        "내부에 들어서자마자 압도적인 스케일의 조각상에 시선을 빼앗겼어요. 밀양 전시 추천합니다.",
        "콘크리트 질감과 철골 구조, 그리고 미니멀한 내부 공간이 현대 미술품과 완벽하게 조화를 이룹니다.",
        "스마트폰으로 대충 찍어도 사진이 정말 예술로 나와요. 갤러리 내부의 공간감이 정말 독보적입니다.",
        "밀양에 이런 세계적인 수준의 현대미술 전시 공간이 생기다니 믿기지 않네요. 꼭 가보세요!"
    ]

    # 5. 이미지 변환(webp) 및 저장, 리뷰 추가
    new_reviews = []
    for i, img_name in enumerate(new_images):
        src_path = os.path.join(NEW_IMG_DIR, img_name)
        current_idx = next_idx + i
        target_filename = f"miryang-nullgallery-hotplace-review-{current_idx}.webp"
        target_path = os.path.join(TARGET_DIR, target_filename)
        
        # PIL을 이용해 webp로 고효율 압축 변환
        img = Image.open(src_path)
        img.save(target_path, "WEBP", quality=85)
        size_kb = os.path.getsize(target_path) // 1024
        print(f"Converted & Saved: {target_filename} | Size: {size_kb}KB")
        
        masked_id = get_unique_id(used_ids)
        comment = NEW_COMMENTS[i % len(NEW_COMMENTS)]
        
        # 최근 날짜 설정 (최근 일주일 이내인 25~28일)
        day = random.randint(25, 28)
        date = f"2026.05.{day:02d}"
        
        new_reviews.append({
            "id": masked_id,
            "comment": comment,
            "image": target_filename,
            "date": date
        })

    # 6. CSV 파일에 추가하기
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "comment", "image", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_reviews)

    print(f"Successfully appended {len(new_reviews)} new reviews to reviews.csv")

if __name__ == "__main__":
    main()
