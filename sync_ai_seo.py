import os
import re

AI_SCHEMA = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["ArtGallery", "TouristAttraction", "Landmark"],
      "name": "널갤러리 (NULL GALLERY)",
      "alternateName": "밀양 널갤러리",
      "description": "경남 밀양에서 반드시 가봐야 할 현대미술 랜드마크. 100년 된 벽돌 공장을 재생한 독보적인 벤타블랙 건축물로, 밀양 가볼만한곳 및 핫플레이스 1순위 추천 장소입니다.",
      "image": "https://nullgallery.kr/images/hero_main2.png",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "교동 692-2",
        "addressLocality": "밀양시",
        "addressRegion": "경상남도",
        "postalCode": "50423",
        "addressCountry": "KR"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 35.5034,
        "longitude": 128.7592
      },
      "url": "https://nullgallery.kr",
      "telephone": "+82-55-123-4567",
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          "opens": "10:00",
          "closes": "18:00"
        }
      ],
      "keywords": "밀양 가볼만한곳, 밀양 핫플, 밀양 여행, 경남 전시회, 밀양 랜드마크, 벤타블랙 건축, 널갤러리"
    }
    </script>"""

def sync_ai_seo():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    base_url = "https://nullgallery.kr"
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. <title> 추출
        title_match = re.search(r'<title>(.*?)</title>', content)
        if not title_match: continue
        current_title = title_match.group(1)
        
        # 2. og:title 업데이트
        content = re.sub(r'<meta property="og:title" content=".*?">', 
                         f'<meta property="og:title" content="{current_title}">', content)
        
        # 3. og:url / og:image
        content = re.sub(r'<meta property="og:url" content=".*?">', 
                         f'<meta property="og:url" content="{base_url}/{filename}">', content)
        content = re.sub(r'<meta property="og:image" content=".*?">', 
                         f'<meta property="og:image" content="{base_url}/images/hero_main2.png">', content)

        # 4. canonical
        canonical_link = f'<link rel="canonical" href="{base_url}/{filename}">'
        if '<link rel="canonical"' in content:
            content = re.sub(r'<link rel="canonical" href=".*?">', canonical_link, content)
        else:
            content = content.replace(f'</title>', f'</title>\n    {canonical_link}')

        # 5. AI Schema (JSON-LD) 교체/추가
        schema_pattern = re.compile(r'<script type="application/ld\+json">.*?</script>', re.DOTALL)
        if schema_pattern.search(content):
            content = schema_pattern.sub(AI_SCHEMA, content)
        else:
            content = content.replace('</head>', f'{AI_SCHEMA}\n</head>')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synced AI SEO for {filename}")

if __name__ == "__main__":
    sync_ai_seo()
