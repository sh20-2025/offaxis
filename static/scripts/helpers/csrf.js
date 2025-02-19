function get_csrf_token() {
    const csrfElement = document.querySelector("input[name=csrfmiddlewaretoken]");
    if (!csrfElement) {
        console.error("CSRF token not found!");
    }
    return csrfElement.value;
}

export { get_csrf_token };
