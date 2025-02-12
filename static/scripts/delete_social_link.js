import { get_csrf_token} from "./helpers/csrf";

document.addEventListener('DOMContentLoaded', function() {
    const deleteIcons = document.querySelectorAll('.delete-social-link');

    deleteIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const socialLinkId = this.getAttribute('data-social-link-id');
            const csrfToken = get_csrf_token();

            fetch(`/delete_social_link/${socialLinkId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ id: socialLinkId })
            })
            .then(response => {
                if (response.ok) {
                    this.parentElement.remove();
                } else {
                    console.error('Failed to delete social link');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
