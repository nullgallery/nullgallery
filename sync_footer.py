import os
import re

CORRECT_EMAIL = "nullgalllery2026@gmail.com" # 3개의 'l'
WRONG_EMAIL = "nullgallery2026@gmail.com"   # 2개의 'l'

STANDARD_FOOTER = """    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-brand">NULL GALLERY</div>
            <div class="footer-cols">
                <div class="footer-col">
                    <p class="footer-col-title">주소</p>
                    <p>경상남도 밀양시 교동 692-2</p>
                </div>
                <div class="footer-col">
                    <p class="footer-col-title">운영시간</p>
                    <p>화 – 일 10:00 – 18:00</p>
                    <p class="footer-muted">월요일 휴관</p>
                </div>
                <div class="footer-col">
                    <p class="footer-col-title">문의</p>
                    <p><a href="mailto:nullgalllery2026@gmail.com">nullgalllery2026@gmail.com</a></p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 NULL GALLERY. All Rights Reserved.</p>
            </div>
        </div>
    </footer>"""

def sync():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 모든 이메일 오타 수정
        content = content.replace(WRONG_EMAIL, CORRECT_EMAIL)
        
        # 2. 푸터 동기화
        # <footer class="footer"> ... </footer> 블록을 찾아서 교체
        footer_pattern = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
        if footer_pattern.search(content):
            content = footer_pattern.sub(STANDARD_FOOTER, content)
        else:
            print(f"Warning: No footer found in {filename}")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synced {filename}")

if __name__ == "__main__":
    sync()
