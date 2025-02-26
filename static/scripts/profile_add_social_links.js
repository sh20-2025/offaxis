import { get_csrf_token } from "./helpers/csrf.js";

document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = get_csrf_token();

    const addLinkButton = document.getElementById("add-social-link-button");
    const typeSelect = document.getElementById("social-type");
    const socialUrl = document.getElementById("social-url");
    const linksContainer = document.getElementById("link-container");

    const urlPatterns = {
        "Facebook": /^https?:\/\/(www\.)?facebook\.com\/.+$/,
        "Twitter": /^https?:\/\/(www\.)?twitter\.com\/.+$/,
        "Instagram": /^https?:\/\/(www\.)?instagram\.com\/.+$/,
        "Youtube": /^https?:\/\/(www\.)?youtube\.com\/.+$/,
        "Spotify": /^https?:\/\/(www\.)?open\.spotify\.com\/.+$/,
        "Soundcloud": /^https?:\/\/(www\.)?soundcloud\.com\/.+$/,
    };

if (addLinkButton) {
        addLinkButton.addEventListener("click", async () => {
            const selectedType = typeSelect.value;
            const url = socialUrl.value;
            const artistSlug = typeSelect.getAttribute("data-artist-slug");

            console.log('testing url pattern', urlPatterns[selectedType].test(url));

            if (!urlPatterns[selectedType].test(url)) {
                alert(`Invalid URL for ${selectedType}`);
                return;
            }

            const data = new FormData();
            data.append("type", selectedType);
            data.append("url", url);
            data.append("artist_slug", artistSlug);

            try {
                const res = await fetch("/add_social_link_on_artist/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                    },
                    body: data,
                });

                const json = await res.json();
                if (json.error) throw new Error(json.error);

                const newLinkLi = document.createElement("li");
                const newLinkA = document.createElement("a");
                newLinkA.href = url;
                newLinkA.innerText = selectedType;
                newLinkLi.appendChild(newLinkA);
                linksContainer.appendChild(newLinkLi);

                // Clear the input fields
                socialUrl.value = "";
                typeSelect.selectedIndex = 0;

                // clear empty message if it exists
                const emptyMessage = document.getElementById("empty-message");
                if (emptyMessage) {
                    emptyMessage.remove();
                }
            } catch (error) {
                alert(error);
            }
        });
    }
});
