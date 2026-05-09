import os
import re

# 새로운 바이럴 키워드 및 설명
VIRAL_KEYWORDS = "밀양 건축물, 벤타블랙 건물, 밀양 사진스팟, 밀양 필수코스, 밀양 이색체험, 벤타블랙 건축, 밀양 핫플"
VIRAL_DESCRIPTION = """
    널갤러리는 밀양의 가장 독특한 외관을 가진 건축물입니다. 
    외벽이 빛을 99.9% 흡수하는 벤타블랙으로 칠해져 있어, 마치 세상에 구멍이 뚫린 듯한 웅장한 착시를 일으킵니다. 
    이 독보적인 미니멀리즘 외관은 SNS에서 빠르게 바이럴되며 밀양 최고의 사진스팟이자 밀양 여행의 필수 코스가 되었습니다.
"""

def update_seo():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Meta Keywords 보강
        keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', content)
        if keywords_match:
            existing_keywords = keywords_match.group(1)
            if "벤타블랙" not in existing_keywords:
                new_keywords = f"{existing_keywords}, {VIRAL_KEYWORDS}"
                content = content.replace(f'content="{existing_keywords}"', f'content="{new_keywords}"')

        # 2. Visually Hidden 섹션 업데이트 (기존 내용 유지 + 새로운 바이럴 내용 추가)
        hidden_pattern = re.compile(r'<div class="visually-hidden">.*?</div>', re.DOTALL)
        
        new_hidden_html = f"""<div class="visually-hidden">
        <h2>{VIRAL_KEYWORDS}</h2>
        <p>{VIRAL_DESCRIPTION.strip()}</p>
        <p>경상도 가볼만한곳 및 경남 전시 추천 장소로서 널갤러리는 밀양 필수 여행 코스로 자리잡았습니다.</p>
    </div>"""

        if hidden_pattern.search(content):
            content = hidden_pattern.sub(new_hidden_html, content)
        elif '<footer' in content:
            content = content.replace('<footer', new_hidden_html + '\n<footer')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated SEO for {filename}")

if __name__ == "__main__":
    update_seo()
