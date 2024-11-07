// Modal elements
var loginModal = document.getElementById('loginModal');
var signupModal = document.getElementById('signupModal');

// Buttons for opening modals from the dropdown
var loginBtn = document.getElementById('loginBtn');
var signupBtn = document.getElementById('signupBtn');

// Close buttons
var closeLogin = document.getElementById('closeLogin');
var closeSignup = document.getElementById('closeSignup');

// Links inside modals for switching
var showLogin = document.getElementById('showLogin');
var showSignUp = document.getElementById('showSignUp');

// Forms
var loginForm = document.querySelector('#loginModal form');
var signupForm = document.querySelector('#signupModal form');

// Error message containers
var loginMessages = document.querySelector('#loginModal .messages');
var signupMessages = document.querySelector('#signupModal .messages');

// Open login modal from the dropdown
loginBtn.onclick = function() {
    loginModal.style.display = "flex";
}

// Open signup modal from the dropdown
signupBtn.onclick = function() {
    signupModal.style.display = "flex";
}

// Close the login modal when clicking on the close button
closeLogin.onclick = function() {
    loginModal.style.display = "none";
}

// Close the signup modal when clicking on the close button
closeSignup.onclick = function() {
    signupModal.style.display = "none";
}

// Show login modal when clicking 'Already have an account?' in the signup modal
showLogin.addEventListener('click', function(event) {
    event.preventDefault();
    signupModal.style.display = "none";  // Hide signup modal
    loginModal.style.display = "flex";   // Show login modal
});

// Show signup modal when clicking 'Don't have an account?' in the login modal
showSignUp.addEventListener('click', function(event) {
    event.preventDefault();
    loginModal.style.display = "none";   // Hide login modal
    signupModal.style.display = "flex";  // Show signup modal
});

// Close modals if user clicks outside modal content
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
    if (event.target == signupModal) {
        signupModal.style.display = "none";
    }
}

// Handle AJAX login form submission
loginForm.onsubmit = async function(event) {
    event.preventDefault();  // Prevent form submission

    // Clear previous messages
    loginMessages.innerHTML = '';

    // Get form data
    const formData = new FormData(loginForm);

    // Send form data via Ajax
    const response = await fetch(loginForm.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',  // Ajax request
        }
    });

    const result = await response.json();

    if (response.ok) {
        // If login is successful, redirect to the main page
        window.location.href = '/';  // Adjust to your desired page
    } else {
        // Display error message in the modal
        loginMessages.innerHTML = `<p>${result.error}</p>`;
    }
};

// Handle AJAX signup form submission
signupForm.onsubmit = async function(event) {
    event.preventDefault();  // Prevent form submission

    // Clear previous messages
    signupMessages.innerHTML = '';

    // Get form data
    const formData = new FormData(signupForm);

    // Send form data via Ajax
    const response = await fetch(signupForm.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',  // Ajax request
        }
    });

    const result = await response.json();

    if (response.ok) {
        // If signup is successful, redirect to the main page
        window.location.href = '/';  // Adjust to your desired page
    } else {
        // Display error message in the modal
        signupMessages.innerHTML = `<p>${result.error}</p>`;
    }
};