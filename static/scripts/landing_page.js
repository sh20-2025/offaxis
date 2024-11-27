document.addEventListener("DOMContentLoaded", function() {
  const headings = document.querySelectorAll(".hero-circle h4");
  console.log(headings);
  headings.forEach(heading => {
    const text = heading.textContent;
    heading.innerHTML = "";
    for (let i = 0; i < text.length; i++) {
      const span = document.createElement("span");
      span.textContent = text[i];
      span.style.transform = `translate(-50%, -780%) rotate(${(-i * 3.2) + (text.length*1.2) + 190}deg) translateY(-160px) scale(-1, -1)`;
      span.style.display = "inline-block";
      span.style.position = "absolute";
      span.style.transformOrigin = "bottom center";

      heading.appendChild(span);
    }
  });
});