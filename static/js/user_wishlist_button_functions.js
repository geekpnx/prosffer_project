
// ---------------- Wish List Icon Botton ----------------------------

// Toggle wishlist dropdown on click
document.getElementById('wishlist-btn').addEventListener('click', function () {
    const wishlistContent = document.getElementById('wishlist-content');
    
    // Toggle display
    if (wishlistContent.style.display === 'block') {
        wishlistContent.style.display = 'none'; // Hide if it's currently shown
    } else {
        wishlistContent.style.display = 'block'; // Show if it's currently hidden
    }
});

// Optional: Close the wishlist if clicking outside of it
document.addEventListener('click', function (event) {
    const wishlistContent = document.getElementById('wishlist-content');
    const wishlistBtn = document.getElementById('wishlist-btn');
    
    // Check if the clicked target is not the wishlist button or its content
    if (!wishlistContent.contains(event.target) && !wishlistBtn.contains(event.target)) {
        wishlistContent.style.display = 'none'; // Hide the dropdown
    }
});


// ---------------- User Icon Botton ----------------------------

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