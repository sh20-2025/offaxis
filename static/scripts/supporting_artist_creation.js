document.addEventListener("DOMContentLoaded", function () {
    const priceInput = document.getElementById("id_gig-price");
    if (priceInput) {
        priceInput.setAttribute("step", "0.01");
        priceInput.setAttribute("min", "0");
    }
});


document.addEventListener("DOMContentLoaded", function () {
    console.log("JS loaded");

    const select = document.getElementById("id_gig-supporting_artists");
    const container = document.getElementById("selected-artists-container");
    const hiddenInput = document.getElementById("supporting_artists_hidden");

    let selectedArtists = [];

    function updateDisplay() {

        container.innerHTML = "";


        selectedArtists.forEach(function (artistId) {

            const option = select.querySelector(`option[value="${artistId}"]`);
            const displayText = option ? option.text : artistId;

            const tag = document.createElement("span");
            tag.classList.add("artist-tag");
            tag.textContent = displayText + " ";


            const removeBtn = document.createElement("button");
            removeBtn.textContent = "×";
            removeBtn.classList.add("remove-tag");
            removeBtn.addEventListener("click", function () {

                selectedArtists = selectedArtists.filter(function (id) {
                    return id !== artistId;
                });
                updateDisplay();
            });

            tag.appendChild(removeBtn);
            container.appendChild(tag);
        });


        hiddenInput.value = selectedArtists.join(",");
    }


    select.addEventListener("change", function () {
        const selectedValue = select.value;
        if (!selectedValue) {
            return;
        }

        if (selectedArtists.indexOf(selectedValue) === -1) {
            if (selectedArtists.length < 5) {
                selectedArtists.push(selectedValue);
            } else {
                alert("You can select up to 5 supporting artists only.");
            }
        }

        select.value = "";
        updateDisplay();
    });


    const form = document.querySelector("form");
    form.addEventListener("submit", function (e) {
        console.log("Submitting supporting artists:", hiddenInput.value);
    });
});
