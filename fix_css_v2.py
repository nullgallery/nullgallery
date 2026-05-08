import os

path = r"E:\02_antigravity\nullgallery_web\style.css"

encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
content = None

for enc in encodings:
    try:
        with open(path, 'r', encoding=enc) as f:
            content = f.read()
        print(f"Read with {enc}")
        break
    except:
        continue

if content:
    # 폰트 오류 수정 (따옴표 누락 및 공백 오류)
    # 기존 코드에서 발견된 오타 패턴들 대응
    content = content.replace('font-family: " Bebas Neue\\, sans-serif;', 'font-family: "Bebas Neue", sans-serif;')
    content = content.replace('font-family: " Bebas Neue", sans-serif;', 'font-family: "Bebas Neue", sans-serif;')
    
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

    if "/*  Reviews  */" in content:
        content = content.split("/*  Reviews  */")[0] + new_reviews_css
    elif "/*  Reviews  */" in content:
        content = content.split("/*  Reviews  */")[0] + new_reviews_css
    else:
        content += new_reviews_css

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully fixed style.css and saved as utf-8")
else:
    print("Failed to read file with any encoding")
