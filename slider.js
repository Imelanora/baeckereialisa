// Diashow für alle Elemente mit der Klasse .slider
// (Pfeile, Punkte, automatisches Weiterblättern, nächstes Bild vorladen)
(function () {
    document.querySelectorAll('.slider').forEach(function (slider) {
        const track = slider.querySelector('.slider-track');
        const slides = track.querySelectorAll('img');
        const interval = parseInt(slider.dataset.interval || '5000', 10);
        if (!slides.length) return;

        const dots = document.createElement('div');
        dots.className = 'slider-dots';
        slides.forEach(function (_, i) {
            const d = document.createElement('button');
            d.className = 'slider-dot' + (i === 0 ? ' active' : '');
            d.setAttribute('aria-label', 'Bild ' + (i + 1));
            d.onclick = function () { go(i); restart(); };
            dots.appendChild(d);
        });
        slider.appendChild(dots);

        ['prev', 'next'].forEach(function (dir) {
            const b = document.createElement('button');
            b.className = 'slider-arrow slider-' + dir;
            b.setAttribute('aria-label', dir === 'prev' ? 'Vorheriges Bild' : 'Nächstes Bild');
            b.innerHTML = dir === 'prev' ? '‹' : '›';
            b.onclick = function () { go(cur + (dir === 'prev' ? -1 : 1)); restart(); };
            slider.appendChild(b);
        });

        let cur = 0;
        if (slides[1]) slides[1].loading = 'eager';

        function go(n) {
            dots.children[cur].classList.remove('active');
            cur = (n + slides.length) % slides.length;
            track.style.transform = 'translateX(-' + cur * 100 + '%)';
            dots.children[cur].classList.add('active');
            slides[cur].loading = 'eager';
            slides[(cur + 1) % slides.length].loading = 'eager';
        }

        let timer = setInterval(function () { go(cur + 1); }, interval);
        function restart() {
            clearInterval(timer);
            timer = setInterval(function () { go(cur + 1); }, interval);
        }
    });
})();
