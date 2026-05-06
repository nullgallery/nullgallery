/* ── null_script.js ─────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {

    // ── 헤더: 랜딩페이지에서 투명 처리 ─────────────────
    const header = document.getElementById('header');
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
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay) {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        }
    });

    // ── Hero 슬라이드쇼 (MP4 → PNG → MP4 → ... 무한루프) ──
    const video = document.getElementById('hero-video');
    const img   = document.getElementById('hero-img');
    const IMG_DISPLAY_MS = 5000; // 이미지 표시 시간 (ms)

    if (video && img) {
        // 영상이 끝나면 → 이미지로 크로스페이드
        video.addEventListener('ended', () => {
            video.classList.remove('active');
            img.classList.add('active');

            // 이미지 5초 후 → 영상으로 다시 크로스페이드 (루프)
            setTimeout(() => {
                img.classList.remove('active');
                video.currentTime = 0;   // 영상 처음으로 되감기
                video.play();
                video.classList.add('active');
            }, IMG_DISPLAY_MS);
        });

        // 영상 로드 실패 시 이미지로 폴백
        video.addEventListener('error', () => {
            video.classList.remove('active');
            img.classList.add('active');
        });
    }

    // ── 전시 필터 탭 ────────────────────────────────────
    const tabs  = document.querySelectorAll('.tab');
    const items = document.querySelectorAll('.ex-item');

    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const filter = tab.dataset.filter;

                items.forEach(item => {
                    const show = filter === 'all' || item.dataset.category === filter;
                    item.style.display = show ? '' : 'none';
                    const next = item.nextElementSibling;
                    if (next && next.classList.contains('ex-divider')) {
                        next.style.display = show ? '' : 'none';
                    }
                });
            });
        });
    }

    // ── 스크롤 페이드인 ─────────────────────────────────
    const fadeEls = document.querySelectorAll('.fade-in');
    if (fadeEls.length > 0) {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => entry.target.classList.add('visible'), i * 80);
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        fadeEls.forEach(el => obs.observe(el));
    }
});
