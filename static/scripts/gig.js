document.addEventListener("DOMContentLoaded", () => {

    const supportArtistForm = document.getElementById('gigForm')
    if (supportArtistForm) {
    supportArtistForm.addEventListener('submit', function (event) {
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
          alert('Support sent successfully! New balance: £' + data.new_balance)
        } else {
          alert(data.error)
        }
      })
      .catch((error) => {
        alert('An error occurred: ' + error.message)
      })
  })
}


const acceptArtistForm = document.getElementById('rejectArtistForm');
if (acceptArtistForm) {    
    acceptArtistForm.addEventListener('submit', function (event) {
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
          alert(data.message)
        } else {
          alert(data.error)
        }
      })
      .catch((error) => {
        alert('An error occurred: ' + error.message)
      })
  })
}


  const rejectArtistForm = document.getElementById('rejectArtistForm');
  if (rejectArtistForm) {
    rejectArtistForm.addEventListener('submit', function (event) {
      event.preventDefault();
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
          alert(data.message)
        } else {
          alert(data.error)
        }
      })
      .catch((error) => {
        alert('An error occurred: ' + error.message)
      })
  })
}

})