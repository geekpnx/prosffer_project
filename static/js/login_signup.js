// Get the modal elements
var loginModal = document.getElementById('loginModal');
var signupModal = document.getElementById('signupModal');

// Get the close buttons
var closeLogin = document.getElementById('closeLogin');
var closeSignup = document.getElementById('closeSignup');

// Function to open a specific modal
function openModal(modalId) {
  var modal = document.getElementById(modalId);
  modal.style.display = 'block';
}

// Function to close the modal
function closeModal(modal) {
  modal.style.display = 'none';
}

// Close the login modal when close button is clicked
closeLogin.onclick = function() {
  closeModal(loginModal);
}

// Close the signup modal when close button is clicked
closeSignup.onclick = function() {
  closeModal(signupModal);
}

// Close the modal if the user clicks anywhere outside the modal
window.onclick = function(event) {
  if (event.target == loginModal) {
    closeModal(loginModal);
  } else if (event.target == signupModal) {
    closeModal(signupModal);
  }
}