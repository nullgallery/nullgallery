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

    // ── Hero 슬라이드쇼 (HERO_MEDIA 기반 무한루프) ──────
    const heroSlideshow = document.querySelector('.hero-slideshow');
    const IMG_DISPLAY_MS = 5000;

    if (heroSlideshow && typeof HERO_MEDIA !== 'undefined' && HERO_MEDIA.length > 0) {
        // 기존 하드코딩된 슬라이드 삭제
        heroSlideshow.innerHTML = '';
        
        let currentIndex = 0;
        const slides = [];

        // 슬라이드 요소 생성
        HERO_MEDIA.forEach((file, idx) => {
            let el;
            if (file.endsWith('.mp4')) {
                el = document.createElement('video');
                el.src = `images/${file}`;
                el.muted = true;
                el.playsInline = true;
                el.preload = 'auto';
                el.className = 'hero-slide hero-slide--video';
            } else {
                el = document.createElement('img');
                el.src = `images/${file}`;
                el.className = 'hero-slide hero-slide--img';
            }
            if (idx === 0) el.classList.add('active');
            heroSlideshow.appendChild(el);
            slides.push(el);
        });

        function nextSlide() {
            const currentSlide = slides[currentIndex];
            currentIndex = (currentIndex + 1) % slides.length;
            const nextSlide = slides[currentIndex];

            currentSlide.classList.remove('active');
            nextSlide.classList.add('active');

            if (nextSlide.tagName === 'VIDEO') {
                nextSlide.currentTime = 0;
                nextSlide.play().catch(e => console.log("Video play blocked:", e));
                nextSlide.onended = nextSlideLogic;
            } else {
                setTimeout(nextSlideLogic, IMG_DISPLAY_MS);
            }
        }

        function nextSlideLogic() {
            nextSlide();
        }

        // 첫 슬라이드가 영상이면 바로 실행
        const first = slides[0];
        if (first.tagName === 'VIDEO') {
            first.play().catch(e => console.log("Video play blocked:", e));
            first.onended = nextSlideLogic;
        } else {
            setTimeout(nextSlideLogic, IMG_DISPLAY_MS);
        }
    }

    // ── 전시 데이터 로드 (CSV) ──────────────────────────
    const exContainer = document.getElementById('exhibition-container');
    const tabs = document.querySelectorAll('.tab');

    if (exContainer) {
        loadExhibitions();
    }

    async function loadExhibitions() {
        try {
            const response = await fetch('exhibitions.csv');
            const data = await response.text();
            const rows = data.split('\n').slice(1).filter(row => row.trim() !== '');
            const exhibitions = rows.map(row => {
                const cols = row.split(',');
                return {
                    id: cols[0],
                    title: cols[1],
                    artist: cols[2],
                    period: cols[3],
                    category: cols[4],
                    folder: cols[5],
                    thumbnail: cols[6]
                };
            });

            renderExhibitions(exhibitions);
            setupFilters(exhibitions);
        } catch (err) {
            console.error('Failed to load exhibitions:', err);
            exContainer.innerHTML = '<p style="text-align:center; padding: 50px;">데이터를 불러오는데 실패했습니다.</p>';
        }
    }

    function renderExhibitions(exhibitions) {
        exContainer.innerHTML = '';
        exhibitions.forEach((ex, index) => {
            const article = document.createElement('article');
            article.className = 'ex-item fade-in';
            article.dataset.category = ex.category;
            article.innerHTML = `
                <a href="javascript:void(0)" class="ex-item-inner" onclick="openGallery('${ex.title}', '${ex.artist}', '${ex.folder}', '${ex.thumbnail}')">
                    <div class="ex-img-wrap">
                        <div class="ex-img" style="background-image:url('images/${ex.thumbnail}');"></div>
                        <div class="ex-badge ${ex.category}">${getCategoryLabel(ex.category)}</div>
                    </div>
                    <div class="ex-meta">
                        <div class="ex-meta-left">
                            <h2>${ex.title}</h2>
                            <p class="ex-artist">${ex.artist}</p>
                            <p class="ex-period">${ex.period}</p>
                        </div>
                        <div class="ex-meta-right"><span class="ex-arrow">→</span></div>
                    </div>
                </a>
            `;
            exContainer.appendChild(article);
            
            if (index < exhibitions.length - 1) {
                const divider = document.createElement('div');
                divider.className = 'ex-divider';
                exContainer.appendChild(divider);
            }
        });
        
        // Re-run intersection observer for new elements
        observeFadeIn();
    }

    function getCategoryLabel(cat) {
        switch(cat) {
            case 'current': return '현재전시';
            case 'upcoming': return '예정전시';
            case 'past': return '과거전시';
            default: return '';
        }
    }

    function setupFilters(exhibitions) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const filter = tab.dataset.filter;

                const items = document.querySelectorAll('.ex-item');
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

    function observeFadeIn() {
        const fadeEls = document.querySelectorAll('.fade-in');
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

    // ── 갤러리 오버레이 ──────────────────────────────────
    window.openGallery = (title, artist, folder, thumb) => {
        const overlay = document.getElementById('gallery-overlay');
        const mainImg = document.getElementById('gallery-main-img');
        const thumbs  = document.getElementById('gallery_thumbs'); // typo check, ID is galleryThumbs in HTML
        const gThumbs  = document.getElementById('galleryThumbs');
        const gTitle  = document.getElementById('galleryTitle');
        const gDesc   = document.getElementById('galleryDesc');

        overlay.classList.add('open');
        mainImg.src = `images/${thumb}`;
        gTitle.innerText = title;
        gDesc.innerText = artist;

        // 폴더 기반 썸네일 로드 (1.jpg ~ 5.jpg 시도)
        gThumbs.innerHTML = '';
        const baseImg = document.createElement('img');
        baseImg.src = `images/${thumb}`;
        baseImg.className = 'active';
        baseImg.onclick = () => {
            mainImg.src = baseImg.src;
            document.querySelectorAll('.gallery-thumbs img').forEach(i => i.classList.remove('active'));
            baseImg.classList.add('active');
        };
        gThumbs.appendChild(baseImg);

        // 추가 이미지 시도 (1.jpg, 2.jpg, 3.jpg...)
        for (let i = 1; i <= 5; i++) {
            const img = new Image();
            const src = `images/${folder}/${i}.jpg`;
            img.src = src;
            img.onload = () => {
                const thumbImg = document.createElement('img');
                thumbImg.src = src;
                thumbImg.onclick = () => {
                    mainImg.src = src;
                    document.querySelectorAll('.gallery-thumbs img').forEach(i => i.classList.remove('active'));
                    thumbImg.classList.add('active');
                };
                gThumbs.appendChild(thumbImg);
            };
        }

        document.body.style.overflow = 'hidden';
    };

    const galleryClose = document.getElementById('galleryClose');
    if (galleryClose) {
        galleryClose.addEventListener('click', () => {
            document.getElementById('gallery-overlay').classList.remove('open');
            document.body.style.overflow = '';
        });
    }

    // ── 스크롤 페이드인 (Initial run) ────────────────────
    observeFadeIn();
});
