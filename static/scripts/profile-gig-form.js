document.addEventListener("DOMContentLoaded", function () {
    const gigFormButton = document.getElementById("add-gig-form-button");
    const gigFormContainer = document.querySelector(".gig-forms-container");

    gigFormButton.addEventListener("click", function () {
        if (gigFormContainer.style.display === "none" || gigFormContainer.style.display === "") {
            gigFormContainer.style.display = "block";
        } else {
            gigFormContainer.style.display = "none";
        }
    });
});
