document.addEventListener("DOMContentLoaded", () => {
    const csrfElement = document.querySelector("input[name=csrfmiddlewaretoken]");
    if (!csrfElement) {
    console.error("CSRF token not found!");
    }
    const csrfToken = csrfElement.value;

    function toggleEditMode(sectionId, editButtonId, saveButtonId, url) {
        const section = document.getElementById(sectionId);
        const editButton = document.getElementById(editButtonId);
        const saveButton = document.getElementById(saveButtonId);
        const artistSlug = editButton.getAttribute("data-artist-slug");

        editButton.addEventListener("click", () => {
            const text = section.innerText;
            section.innerHTML = `<textarea id="${sectionId}-textarea" class="editable-textarea">${text}</textarea>`;
            editButton.style.display = "none";
            saveButton.style.display = "inline";

            const textarea = document.getElementById(`${sectionId}-textarea`);
            textarea.addEventListener("keydown", (event) => {
                if (event.key === "Enter") { // Enter key
                    event.preventDefault();
                    saveButton.click();
                }
            });
        });

        saveButton.addEventListener("click", async () => {
            const textarea = document.getElementById(`${sectionId}-textarea`);
            const newText = textarea.value;

            const data = new FormData();
            data.append("section_id", sectionId);
            data.append("new_text", newText);
            data.append("artist_slug", artistSlug);

            console.log(url)
            try {
                const res = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                    },
                    body: data,
                });

                const json = await res.json();
                if (json.error) throw new Error(json.error);

                section.innerText = newText;
                editButton.style.display = "inline";
                saveButton.style.display = "none";
            } catch (error) {
                alert(error);
            }
        });
    }


    if (document.getElementById("edit-bio-button")) {
    toggleEditMode("bio-text", "edit-bio-button",
        "save-bio-button", "/update_text/");
  }
});