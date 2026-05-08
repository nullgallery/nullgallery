import os

path = r"E:\02_antigravity\nullgallery_web\style.css"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS 문법 오류 수정 (따옴표 누락 및 오타)
content = content.replace('font-family: " Bebas Neue\\, sans-serif;', 'font-family: "Bebas Neue", sans-serif;')

# 리뷰 그리드 및 카드 스타일 강화
new_reviews_css = """
/* ── Reviews ────────────────────────── */
.reviews-main { padding: 80px 5%; background: #fff; }
.reviews-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
    gap: 32px 24px; 
    max-width: 1400px; 
    margin: 0 auto; 
}
.review-card { 
    background: #fff; 
    border: 1px solid #eee; 
    overflow: hidden; 
    transition: transform 0.3s ease, box-shadow 0.3s ease; 
    display: flex; 
    flex-direction: column; 
}
.review-card:hover { transform: translateY(-8px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }
.review-img-wrap { 
    width: 100%; 
    aspect-ratio: 3 / 4; 
    overflow: hidden; 
    background: #f5f5f5;
}
.review-img-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
.review-card:hover .review-img-wrap img { transform: scale(1.05); }
.review-body { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }
.review-text { 
    font-size: 14px; 
    line-height: 1.6; 
    color: #333; 
    margin-bottom: 16px; 
    flex-grow: 1;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.review-meta { 
    border-top: 1px solid #f0f0f0; 
    padding-top: 12px; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
}
.review-author { font-weight: 700; font-size: 13px; color: #000; letter-spacing: 0.5px; }
.review-date { font-size: 11px; color: #999; }
"""

# 기존 리뷰 섹션 찾아서 교체 (없으면 끝에 추가)
if "/*  Reviews  */" in content:
    content = content.split("/*  Reviews  */")[0] + new_reviews_css
else:
    content += new_reviews_css

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully fixed style.css")
