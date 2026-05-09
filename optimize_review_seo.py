import os
import pandas as pd

def optimize_images_for_seo():
    review_img_dir = r"E:\02_antigravity\nullgallery_web\images\reviews"
    csv_path = r"E:\02_antigravity\nullgallery_web\reviews.csv"
    
    # 1. CSV 로드
    df = pd.read_csv(csv_path)
    
    # 2. 파일 이름 변경 및 데이터프레임 업데이트
    new_images = []
    for idx, row in df.iterrows():
        old_name = row['image']
        # 키워드 조합: miryang-nullgallery-hotplace-review-1.png
        new_name = f"miryang-nullgallery-hotplace-review-{idx+1}.png"
        
        old_path = os.path.join(review_img_dir, old_name)
        new_path = os.path.join(review_img_dir, new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
        else:
            print(f"File not found: {old_path}")
            
        new_images.append(new_name)
    
    df['image'] = new_images
    df.to_csv(csv_path, index=False)
    print("CSV updated successfully.")

if __name__ == "__main__":
    optimize_images_for_seo()
