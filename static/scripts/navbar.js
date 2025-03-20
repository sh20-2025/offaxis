document.addEventListener("DOMContentLoaded", () => {
  const scriptTag = document.querySelector('script[src*="navbar.js"]');
  const staticUrl = scriptTag.getAttribute("data-static-url");

  const hamburgerButton = document.getElementById("hamburgerButton");
  const navbar = document.getElementById("navbar-header-container");
  const nav = document.querySelector(".nav");
  const svgIcon = document.getElementById("hamburgerMenuSVG"); // This is an <img> element
  const headerPlaceholder = document.querySelector(".header-scroll-placeholder");

  hamburgerButton.addEventListener("click", () => {
    const active = nav.classList.toggle("active");
    if (active) {
      navbar.classList.add("open");
    } else {
      navbar.classList.remove("open");
    }

    // Update the `src` attribute for the <img> tag
    const currentSrc = svgIcon.getAttribute("src");
    if (currentSrc === `${staticUrl}icons/hamburger-menu.svg`) {
      svgIcon.setAttribute("src", `${staticUrl}icons/close-button.svg`);
    } else {
      svgIcon.setAttribute("src", `${staticUrl}icons/hamburger-menu.svg`);
    }
  });

  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;
    if (scrollPosition > 50) {
      navbar.classList.add("scrolled");
      headerPlaceholder.classList.add("scrolled");
      headerPlaceholder.style.height = `${navbar.clientHeight}px`;
    } else {
      navbar.classList.remove("scrolled");
      headerPlaceholder.classList.remove("scrolled");
    }
  });
});
