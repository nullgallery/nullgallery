/* ── null_script.js ─────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {

    // ── 헤더 스크롤 효과 ────────────────────────────────
    const header = document.getElementById('header');
    if (header && header.classList.contains('transparent')) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 60) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // ── 랜딩 히어로 헤더 투명 처리 ─────────────────────
    if (header && !document.body.classList.contains('page-inner')) {
        header.classList.add('transparent');
        window.addEventListener('scroll', () => {
            if (window.scrollY > window.innerHeight * 0.6) {
                header.classList.add('scrolled');
                header.classList.remove('transparent');
            } else {
                header.classList.remove('scrolled');
                header.classList.add('transparent');
            }
        });
    }

    // ── 메뉴 오버레이 ───────────────────────────────────
    const menuBtn   = document.getElementById('menuBtn');
    const menuClose = document.getElementById('menuClose');
    const overlay   = document.getElementById('menuOverlay');

    if (menuBtn && overlay) {
        menuBtn.addEventListener('click', () => {
            overlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        });
    }
    if (menuClose && overlay) {
        menuClose.addEventListener('click', () => {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        });
    }
    // ESC로 닫기
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay) {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        }
    });

    // ── 전시 필터 탭 ────────────────────────────────────
    const tabs  = document.querySelectorAll('.tab');
    const items = document.querySelectorAll('.ex-item');
    const dividers = document.querySelectorAll('.ex-divider');

    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // 탭 활성화
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                const filter = tab.dataset.filter;

                // 아이템 필터링
                let prevVisible = null;
                items.forEach((item, i) => {
                    const cat = item.dataset.category;
                    const show = filter === 'all' || cat === filter;

                    item.style.display = show ? '' : 'none';

                    // 구분선 처리 (아이템 바로 다음 divider)
                    const nextEl = item.nextElementSibling;
                    if (nextEl && nextEl.classList.contains('ex-divider')) {
                        nextEl.style.display = show ? '' : 'none';
                    }
                });
            });
        });
    }

    // ── Intersection Observer 스크롤 페이드인 ──────────
    const fadeEls = document.querySelectorAll('.fade-in');
    if (fadeEls.length > 0) {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, i * 80);
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        fadeEls.forEach(el => obs.observe(el));
    }

});
