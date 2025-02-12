import { get_csrf_token} from "./helpers/csrf";

document.addEventListener("DOMContentLoaded", () => {
  const csrfToken = get_csrf_token();

  async function uploadImage(inputElement, url, imgElement, artistSlug = null,) {
    const file = inputElement.files[0];

    // Check file type
    if (file.type !== "image/jpeg" && file.type !== "image/png") {
      alert("Error: Image must be a png or jpeg.");
      return;
    }

    // Check file size (limit to 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      alert("Error: Image must be less than 5MB.");
      return;
    }

    const data = new FormData();


    data.append("artist_slug", artistSlug);
    data.append("profile_picture", file); // Ensure the name matches the expected name in the view


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

      imgElement.src = json.picture_url; // Update the image source
    } catch (error) {
      alert(error);
    }
  }

  const customUploadButton = document.getElementById("custom-upload-button");
  const profilePictureInput = document.getElementById("upload-picture");
  const profilePictureImg = document.querySelector(".profile-picture img");
  if (customUploadButton) {
    customUploadButton.addEventListener("click", () => {
      profilePictureInput.click();
    });
  }
  if (profilePictureInput) {
      const artistSlug = profilePictureInput.getAttribute("data-artist-slug");
    profilePictureInput.addEventListener("input", () => {
      uploadImage(profilePictureInput, "/upload_profile_picture/", profilePictureImg, artistSlug).then(r => {
      });
    });
  }
});
