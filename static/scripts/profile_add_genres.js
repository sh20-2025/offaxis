import {get_csrf_token} from "./helpers/csrf.js";

document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = get_csrf_token();

    const addGenreButton = document.getElementById("add-genre-button");
    const genreSelect = document.getElementById("genre");
    const genreTagsContainer = document.getElementById("genre-tags");

    if (addGenreButton) {
        addGenreButton.addEventListener("click", async () => {
            const selectedGenre = genreSelect.value;

            const artistSlug = genreSelect.getAttribute("data-artist-slug");

            const data = new FormData();
            data.append("genre", selectedGenre);
            data.append("artist_slug", artistSlug);

            try {
                const res = await fetch("/add_genre/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                    },
                    body: data,
                });

                const json = await res.json();
                if (json.error) throw new Error(json.error);

                const newGenreDiv = document.createElement("div");
                newGenreDiv.className = "genre";
                newGenreDiv.innerText = selectedGenre;
                genreTagsContainer.appendChild(newGenreDiv);
            } catch (error) {
                alert(error);
            }
        });
    }
});
