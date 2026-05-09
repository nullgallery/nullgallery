import os
import re

KEYWORDS = "경상도 가볼만한곳, 경상도 핫플, 경상도 전시 추천, 경남 가볼만한곳, 경남 전시회, 경남 갤러리, 경남 여행 코스, 밀양 널갤러리"

HIDDEN_SEO_HTML = f"""
    <!-- SEO Keywords (Hidden) -->
    <div class="visually-hidden">
        <h2>{KEYWORDS}</h2>
        <p>널갤러리는 경상도 밀양의 현대미술 공간으로, 경상도 가볼만한곳 및 경남 전시 추천 장소입니다. 경상도 핫플을 찾는 방문객들에게 최고의 예술 경험을 선사합니다.</p>
    </div>
"""

def update_html():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Meta keywords 업데이트
        content = re.sub(r'<meta name="keywords" content=".*?">', 
                        f'<meta name="keywords" content="{KEYWORDS}, 밀양 갤러리, 밀양 데이트">', content)
        
        # 2. 이미지/영상 alt 태그에 키워드 추가 (기존 alt 유지하며 추가)
        def add_keywords(match):
            tag = match.group(0)
            if 'alt="' in tag:
                tag = tag.replace('alt="', f'alt="경상도 가볼만한곳 핫플 추천 - ')
            else:
                tag = tag.replace('img ', 'img alt="경상도 가볼만한곳 핫플 - 널갤러리" ')
            return tag
        
        content = re.sub(r'<img .*?>', add_keywords, content)
        
        # 3. 숨겨진 키워드 섹션 추가 (footer 바로 앞에)
        if '<footer' in content and 'visually-hidden' not in content:
            content = content.replace('<footer', HIDDEN_SEO_HTML + '<footer')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML: {filename}")

def update_js():
    js_path = 'script.js'
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 전시 및 리뷰 동적 생성 시 alt 태그 강화
        content = content.replace('alt="${seoAlt}"', 'alt="[경상도 전시 추천] ${seoAlt}"')
        content = content.replace('alt="${ex.title}"', 'alt="[경상도 가볼만한곳] ${ex.title} - 널갤러리"')
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated JS: {js_path}")

if __name__ == "__main__":
    update_html()
    update_js()
