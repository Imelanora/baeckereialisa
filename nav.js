(function () {
    const pages = [
        { label: 'Start', file: 'index.html' },
        { label: 'Showroom', file: 'showroom.html' },
        { label: 'Events', file: 'events.html' },
        { label: 'Speisekarte', file: 'speisekarte.html' },
        { label: 'Bestellen', file: 'bestellen.html' },
        { label: 'Kontakt', file: 'kontakt.html' },
    ];

    const currentFile = location.pathname.split('/').pop() || 'index.html';
    // Detect if we're in a subfolder (e.g. rechtliches/)
    const inSub = location.pathname.includes('/rechtliches/');
    const base = inSub ? '../' : '';

    const navHTML = `
<nav id="main-nav">
    <div class="nav-inner">
        <a class="nav-logo" href="${base}index.html">
            <img src="${base}logo.png" alt="Bäckerei Alisa" style="height:70px;width:auto;display:block;" />
        </a>
        <ul class="nav-links">
            ${pages.map(p => `
            <li><a href="${base}${p.file}"
                    class="${currentFile === p.file || (currentFile === '' && p.file === 'index.html') ? 'active' : ''}">${p.label}</a>
            </li>
            `).join('')}
        </ul>
        <button class="nav-burger" id="nav-burger" aria-label="Menü öffnen">
            <span></span><span></span><span></span>
        </button>
    </div>
    <div class="nav-mobile-menu" id="nav-mobile-menu">
        ${pages.map(p => `
        <a href="${base}${p.file}"
            class="${currentFile === p.file || (currentFile === '' && p.file === 'index.html') ? 'active' : ''}">${p.label}</a>
        `).join('')}
    </div>
</nav>`;

    document.body.insertAdjacentHTML('afterbegin', navHTML);

    const burger = document.getElementById('nav-burger');
    const mobileMenu = document.getElementById('nav-mobile-menu');

    burger.addEventListener('click', () => {
        const open = mobileMenu.classList.toggle('open');
        burger.classList.toggle('open', open);
    });

    mobileMenu.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
            mobileMenu.classList.remove('open');
            burger.classList.remove('open');
        });
    });
})();