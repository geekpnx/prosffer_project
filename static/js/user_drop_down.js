document.getElementById("user-icon-btn").addEventListener("click", function(event) {
    event.stopPropagation();  // Prevents the click from propagating to other elements
    var dropdown = document.getElementById("dropdown-content");
    dropdown.classList.toggle("show"); // Toggles the dropdown menu
});

// Close the dropdown if the user clicks outside
window.onclick = function(event) {
    if (!event.target.closest('#user-icon-btn')) {
        var dropdown = document.getElementById("dropdown-content");
        dropdown.classList.remove("show");
    }
};