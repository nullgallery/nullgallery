import os

base_dir = r"E:\02_antigravity\nullgallery_web"
script_js_path = os.path.join(base_dir, "script.js")
style_css_path = os.path.join(base_dir, "style.css")

js_code = """
    // ── 진실 팝업 (예약 클릭 시) ─────────────────────────
    const truthOverlay = document.createElement('div');
    truthOverlay.id = 'truthOverlay';
    truthOverlay.innerHTML = `
        <div class="truth-modal">
            <button class="truth-close" id="truthClose">✕</button>
            <div class="truth-content">
                <h2>아직 없는 장소입니다.</h2>
                <p>안녕하세요 홍익대학교 건축학과 박경민이라고 합니다.</p>
                <p>"디지털 이미지가 오늘날 장소를 존재하게 한다."라는 주제로 프로젝트를 진행 중 입니다.</p>
                <p>그래서 몇십년간 폐허였던 장소를 AI를 통해 살아있는 것 처럼 만들고 장소핀을 구글맵에 노출시켰으며 광고를 했습니다.</p>
                <p>귀한 시간 내주셔서 정말 감사하고 죄송합니다.</p>
                <p>구글맵에는 이 장소에 등장한 다른 컨셉의 핀이 옆에 있습니다. 시간 되시면 장소핀을 클릭해보세요.</p>
            </div>
        </div>
    `;
    document.body.appendChild(truthOverlay);

    const truthCloseBtn = document.getElementById('truthClose');
    truthCloseBtn.addEventListener('click', () => {
        truthOverlay.classList.remove('open');
    });

    document.querySelectorAll('a[href="reservation.html"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            truthOverlay.classList.add('open');
            // 만약 메뉴 오버레이가 열려있다면 닫아줌
            const menuOverlay = document.getElementById('menuOverlay');
            if (menuOverlay && menuOverlay.classList.contains('open')) {
                menuOverlay.classList.remove('open');
                document.body.style.overflow = '';
            }
        });
    });
"""

css_code = """
/* ── 진실 팝업 오버레이 ────────────────────────────── */
#truthOverlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.9);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s ease;
}
#truthOverlay.open {
    opacity: 1;
    pointer-events: auto;
}
.truth-modal {
    background: #000;
    color: #fff;
    border: 1px solid #333;
    padding: 3rem 2rem;
    max-width: 500px;
    width: 90%;
    text-align: center;
    position: relative;
    transform: translateY(20px);
    transition: transform 0.4s ease;
}
#truthOverlay.open .truth-modal {
    transform: translateY(0);
}
.truth-close {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    line-height: 1;
}
.truth-content h2 {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}
.truth-content p {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: #ccc;
    word-break: keep-all;
}
.truth-content p:last-child {
    margin-bottom: 0;
}
"""

with open(script_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Insert before the last });
if js_content.endswith("});\n"):
    js_content = js_content[:-4] + js_code + "});\n"
else:
    js_content += js_code

with open(script_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

with open(style_css_path, 'a', encoding='utf-8') as f:
    f.write(css_code)

print("Popup logic added to script.js and style.css")
