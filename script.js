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
        heroSlideshow.innerHTML = '';
        let currentIndex = 0;
        const slides = [];

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
        function nextSlideLogic() { nextSlide(); }

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
    const indexGrid = document.getElementById('index-ex-grid');
    const tabs = document.querySelectorAll('.tab');

    if (exContainer || indexGrid) { loadExhibitions(); }

    async function loadExhibitions() {
        try {
            const response = await fetch('exhibitions.csv');
            const data = await response.text();
            const rows = data.split('\n').slice(1).filter(row => row.trim() !== '');
            const exhibitions = rows.map(row => {
                const cols = row.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
                return { 
                    id: cols[0], 
                    title: cols[1].replace(/"/g, ''), 
                    artist: cols[2].replace(/"/g, ''), 
                    period: cols[3].replace(/"/g, ''), 
                    category: cols[4].replace(/"/g, ''), 
                    folder: cols[5].replace(/"/g, ''), 
                    thumbnail: cols[6].replace(/"/g, ''),
                    url: cols[7] ? cols[7].replace(/"/g, '').trim() : '#'
                };
            });
            
            // Hero Section Rendering
            const heroTitle = document.getElementById('hero-title');
            const heroDate = document.getElementById('hero-date');
            if (heroTitle && heroDate && exhibitions.length > 0) {
                const mainEx = exhibitions.find(ex => ex.category === 'current' || ex.category === 'upcoming') || exhibitions[0];
                let formattedTitle = mainEx.title;
                // ":" 기준으로 줄바꿈 처리 (예: "RON MUECK: 생명의 무게")
                if (formattedTitle.includes(':')) {
                    const parts = formattedTitle.split(':');
                    formattedTitle = `${parts[0]}<br><em>${parts[1].trim()}</em>`;
                }
                heroTitle.innerHTML = formattedTitle;
                heroDate.textContent = mainEx.period;
                const heroCTA = document.querySelector('.hero-cta');
                if (heroCTA && mainEx.url !== '#') {
                    heroCTA.href = mainEx.url;
                }
            }

            // Exhibition Page Rendering
            if (exContainer) {
                renderExhibitions(exhibitions);
                setupFilters();
            }

            // Landing Page Rendering
            const indexGrid = document.getElementById('index-ex-grid');
            if (indexGrid) {
                indexGrid.innerHTML = '';
                exhibitions.filter(ex => ex.category === 'current' || ex.category === 'upcoming').forEach(ex => {
                    const cardHTML = `
                        <a href="${ex.url === '#' ? 'exhibition.html' : ex.url}" class="exhibit-card">
                            <div class="exhibit-img-wrap">
                                <div class="exhibit-img" style="background-image:url('images/${ex.thumbnail}'); background-color:#1a1a1a;"></div>
                            </div>
                            <div class="exhibit-info">
                                <p class="exhibit-label">${getCategoryLabel(ex.category)}</p>
                                <h3>${ex.title}</h3>
                                <p class="exhibit-period">${ex.period}</p>
                                <p class="exhibit-venue">NULL GALLERY, 밀양</p>
                            </div>
                        </a>
                    `;
                    indexGrid.insertAdjacentHTML('beforeend', cardHTML);
                });
            }
        } catch (err) { console.error('Exhibition Load Error:', err); }
    }

    function renderExhibitions(exhibitions) {
        exContainer.innerHTML = '';
        exhibitions.forEach((ex, index) => {
            const article = document.createElement('article');
            article.className = 'ex-item fade-in';
            article.dataset.category = ex.category;
            
            const isExternal = ex.url !== '#';
            const clickAction = isExternal 
                ? `location.href='${ex.url}'` 
                : `openGallery('${ex.title}', '${ex.artist}', '${ex.folder}', '${ex.thumbnail}')`;

            article.innerHTML = `
                <a href="${ex.url === '#' ? 'javascript:void(0)' : ex.url}" class="ex-item-inner" onclick="${ex.url === '#' ? clickAction : ''}">
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
        observeFadeIn();
    }

    function getCategoryLabel(cat) {
        if (cat === 'current') return '현재전시';
        if (cat === 'upcoming') return '예정전시';
        if (cat === 'past') return '과거전시';
        return '';
    }

    function setupFilters() {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const filter = tab.dataset.filter;
                document.querySelectorAll('.ex-item').forEach(item => {
                    const show = filter === 'all' || item.dataset.category === filter;
                    item.style.display = show ? '' : 'none';
                    const next = item.nextElementSibling;
                    if (next && next.classList.contains('ex-divider')) next.style.display = show ? '' : 'none';
                });
            });
        });
    }

    // ── 갤러리 오버레이 ──────────────────────────────────
    window.openGallery = (title, artist, folder, thumb) => {
        const overlay = document.getElementById('gallery-overlay');
        const mainImg = document.getElementById('gallery-main-img');
        const gThumbs = document.getElementById('galleryThumbs');
        const gTitle  = document.getElementById('galleryTitle');
        const gDesc   = document.getElementById('galleryDesc');

        overlay.classList.add('open');
        mainImg.src = `images/${thumb}`;
        gTitle.innerText = title;
        gDesc.innerText = artist;

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

        for (let i = 1; i <= 8; i++) {
            const src = `images/${folder}/${i}.jpg`;
            const imgCheck = new Image();
            imgCheck.src = src;
            imgCheck.onload = () => {
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

    // ── 방문후기 로드 (CSV) ──────────────────────────
    const revContainer = document.getElementById('reviews-container');
    if (revContainer) { loadReviews(); }

    async function loadReviews() {
        try {
            const response = await fetch('reviews.csv');
            const data = await response.text();
            const rows = data.split('\n').slice(1).filter(row => row.trim() !== '');
            revContainer.innerHTML = '';
            
            rows.forEach(row => {
                const cols = row.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
                if (cols.length < 3) return;

                const id = cols[0].replace(/"/g, '').trim();
                const comment = cols[1].replace(/"/g, '').trim();
                const image = cols[2].replace(/"/g, '').trim();
                const date = cols[3] ? cols[3].replace(/"/g, '').trim() : '';
                
                const card = document.createElement('div');
                card.className = 'review-card fade-in';
                
                // SEO용 키워드 조합
                const seoAlt = `밀양 널갤러리 후기 - ${comment.substring(0, 20)}... 밀양 현대전시, 밀양 전시, 밀양 신상갤러리, 밀양 핫플 추천`;

                card.innerHTML = `
                    <div class="review-img-wrap">
                        <img src="images/reviews/${image}" alt="${seoAlt}" loading="lazy">
                        <div class="review-insta-icon">
                            <svg viewBox="0 0 24 24" fill="#fff"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28-.073-1.689-.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                        </div>
                    </div>
                    <div class="review-body">
                        <p class="review-text">${comment}</p>
                        <div class="review-meta">
                            <span class="review-author">${id}</span>
                            <span class="review-date">${date}</span>
                        </div>
                    </div>
                `;
                revContainer.appendChild(card);
            });

            if (window.instgrm) {
                window.instgrm.Embeds.process();
            }

            observeFadeIn();
        } catch (err) { console.error('Review Load Error:', err); }
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

    observeFadeIn();
});
