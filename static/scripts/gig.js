document.addEventListener("DOMContentLoaded", function() {
  const supportForm = document.getElementById('supportArtistForm');
  if (supportForm) {
    supportForm.addEventListener('submit', function (event) {
      event.preventDefault()
      const formData = new FormData(this)
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert('Support sent successfully! New balance: ' + data.new_balance + ' credits.')
          } else {
            alert(data.error)
          }
        })
        .catch((error) => {
          alert('An error occurred: ' + error.message)
        })
    });
  }

  document.querySelectorAll('form[id^="acceptArtistForm_"]').forEach(form => {
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(this);
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert(data.message);
          } else {
            alert(data.error);
          }
        })
        .catch((error) => {
          alert('An error occurred: ' + error.message);
        });
    });
  });
  
  document.querySelectorAll('form[id^="rejectArtistForm_"]').forEach(form => {
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(this);
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert(data.message);
          } else {
            alert(data.error);
          }
        })
        .catch((error) => {
          alert('An error occurred: ' + error.message);
        });
    });
  });
});