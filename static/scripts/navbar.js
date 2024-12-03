document.addEventListener('DOMContentLoaded', () => {
    const scriptTag = document.querySelector('script[src*="navbar.js"]');
    const staticUrl = scriptTag.getAttribute('data-static-url');

    const hamburgerButton = document.getElementById('hamburgerButton');
    const nav = document.querySelector('.nav');
    const svgIcon = document.getElementById('hamburgerMenuSVG'); // This is an <img> element

    hamburgerButton.addEventListener('click', () => {
        nav.classList.toggle('active');

        // Update the `src` attribute for the <img> tag
        const currentSrc = svgIcon.getAttribute('src');
        if (currentSrc === `${staticUrl}icons/hamburger-menu.svg`) {
            svgIcon.setAttribute('src', `${staticUrl}icons/close-button.svg`);
        } else {
            svgIcon.setAttribute('src', `${staticUrl}icons/hamburger-menu.svg`);
        }
    });

    const navbar = document.getElementById('navbar-header-container');
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        if (scrollPosition > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});
