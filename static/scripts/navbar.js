document.addEventListener('DOMContentLoaded', () => {
    const hamburgerButton = document.getElementById('hamburgerButton');
    const nav = document.querySelector('.nav');


    hamburgerButton.addEventListener('click', () => {
        nav.classList.toggle('active');
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
