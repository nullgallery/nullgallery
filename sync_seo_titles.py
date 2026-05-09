import os
import re

def sync_seo():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    base_url = "https://nullgallery.kr"
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. <title> 추출
        title_match = re.search(r'<title>(.*?)</title>', content)
        if not title_match:
            continue
        current_title = title_match.group(1)
        
        # 2. og:title 업데이트 (메인 타이틀과 동일하게)
        content = re.sub(r'<meta property="og:title" content=".*?">', 
                         f'<meta property="og:title" content="{current_title}">', 
                         content)
        
        # 3. og:url 업데이트 (nullgallery.kr 도메인으로)
        content = re.sub(r'<meta property="og:url" content=".*?">', 
                         f'<meta property="og:url" content="{base_url}/{filename}">', 
                         content)
        # 만약 og:url이 없다면 추가
        if '<meta property="og:url"' not in content:
            content = content.replace('</head>', f'    <meta property="og:url" content="{base_url}/{filename}">\n</head>')

        # 4. og:image 업데이트 (nullgallery.kr 도메인으로)
        content = re.sub(r'<meta property="og:image" content="https://nullgallery\.github\.io/.*?">', 
                         f'<meta property="og:image" content="{base_url}/images/hero_main2.png">', 
                         content)

        # 5. canonical link 추가/업데이트
        canonical_link = f'<link rel="canonical" href="{base_url}/{filename}">'
        if '<link rel="canonical"' in content:
            content = re.sub(r'<link rel="canonical" href=".*?">', canonical_link, content)
        else:
            # <title> 바로 뒤에 삽입
            content = content.replace(f'</title>', f'</title>\n    {canonical_link}')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synced SEO for {filename}")

if __name__ == "__main__":
    sync_seo()
