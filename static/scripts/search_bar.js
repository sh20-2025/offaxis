const searchBarInput = document.getElementById("search-bar");
const searchElements = Array.from(document.querySelectorAll("[data-search]"));

searchBarInput.addEventListener("keyup", (e) => {
  const searchValue = e.target.value.toLowerCase();
  const matchedSearchElements = Array.from(searchElements).filter((element) => {
    const value = element.getAttribute("data-search").toLowerCase();
    return value.includes(searchValue);
  });

  searchElements.forEach((element) => {
    element.style.display = "none";
  });

  matchedSearchElements.forEach((element) => {
    element.style.display = "block";
  });
});
