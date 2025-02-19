const modals = document.querySelectorAll(".modal");

modals.forEach((modal) => {
  const closeButtons = modal.querySelectorAll(".modal-close");

  closeButtons.forEach((closeButton) => {
    closeButton.addEventListener("click", () => {
      modal.classList.remove("modal--open");
    });
  });

  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.classList.remove("modal--open");
    }
  });
});

export function openModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.add("modal--open");
}

export function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.remove("modal--open");
}
