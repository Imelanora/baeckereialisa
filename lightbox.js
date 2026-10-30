// Vergrößerte Ansicht für Fotos in .photo-grid (Klick öffnet, Pfeile blättern, Esc schließt)
// und "Mehr anzeigen"-Knöpfe für Raster mit ausgeblendeten Fotos.
(function () {
    const box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML =
        '<button class="lightbox-close" aria-label="Schließen">×</button>' +
        '<button class="lightbox-arrow lightbox-prev" aria-label="Vorheriges Foto">‹</button>' +
        '<img alt="" />' +
        '<button class="lightbox-arrow lightbox-next" aria-label="Nächstes Foto">›</button>';
    document.body.appendChild(box);
    const big = box.querySelector('img');
    let list = [], cur = 0;

    function show(i) {
        cur = (i + list.length) % list.length;
        big.src = list[cur].currentSrc || list[cur].src;
        big.alt = list[cur].alt;
    }
    function close() {
        box.classList.remove('open');
        document.body.style.overflow = '';
    }

    document.querySelectorAll('.photo-grid').forEach(function (grid) {
        const imgs = Array.from(grid.querySelectorAll('img'));
        imgs.forEach(function (img, i) {
            img.addEventListener('click', function () {
                list = imgs.filter(function (x) { return x.offsetParent !== null; });
                show(list.indexOf(img));
                box.classList.add('open');
                document.body.style.overflow = 'hidden';
            });
        });
    });

    box.querySelector('.lightbox-prev').onclick = function (e) { e.stopPropagation(); show(cur - 1); };
    box.querySelector('.lightbox-next').onclick = function (e) { e.stopPropagation(); show(cur + 1); };
    box.querySelector('.lightbox-close').onclick = close;
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') show(cur - 1);
        if (e.key === 'ArrowRight') show(cur + 1);
    });

    document.querySelectorAll('[data-show-more]').forEach(function (btn) {
        const grid = document.getElementById(btn.dataset.showMore);
        btn.addEventListener('click', function () {
            grid.classList.add('show-all');
            btn.remove();
        });
    });
})();
