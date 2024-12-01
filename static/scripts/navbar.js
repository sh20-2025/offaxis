document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar-header-container');
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercentage = (scrollPosition / pageHeight) * 100;

        if (scrollPercentage > 5) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});
