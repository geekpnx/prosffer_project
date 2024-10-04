// ---------------- Wish List Icon Button ----------------------------

// Toggle wishlist dropdown on click
// Flag to check if the wishlist is open
let isWishlistOpen = false;

// Toggle wishlist visibility
document.getElementById('wishlist-btn').addEventListener('click', function(event) {
    event.stopPropagation();  // Prevent click from closing other dropdowns
    const wishlistContent = document.getElementById('wishlist-content');
    
    // Toggle display of wishlist
    if (isWishlistOpen) {
        wishlistContent.style.display = 'none'; // Hide if currently open
        isWishlistOpen = false;
    } else {
        wishlistContent.style.display = 'block'; // Show if currently hidden
        isWishlistOpen = true;
    }
    
    // Ensure the user dropdown closes if it was open
    document.getElementById('user-dropdown-content').classList.remove('show');
});

// Close wishlist dropdown if user clicks outside
document.addEventListener('click', function(event) {
    const wishlistContent = document.getElementById('wishlist-content');
    const wishlistBtn = document.getElementById('wishlist-btn');
    
    // Close wishlist dropdown if clicked outside
    if (isWishlistOpen && !wishlistContent.contains(event.target) && !wishlistBtn.contains(event.target)) {
        wishlistContent.style.display = 'none';
        isWishlistOpen = false;
    }
});

// Prevent closing the dropdown when interacting with the wishlist
const wishlistDropdown = document.getElementById('wishlist-content');
wishlistDropdown.addEventListener('click', function(event) {
    event.stopPropagation();  // Prevent the dropdown from closing when interacting inside
});


// ---------------- User Icon Button ----------------------------

document.getElementById("user-icon-btn").addEventListener("click", function(event) {
    event.stopPropagation();  // Prevent click from closing other dropdowns
    const dropdown = document.getElementById("user-dropdown-content");
    
    // Toggle display
    if (dropdown.classList.contains("show")) {
        dropdown.classList.remove("show"); // Hide if it's currently shown
    } else {
        dropdown.classList.add("show"); // Show if it's currently hidden
    }

    // Ensure the wishlist closes if it was open
    document.getElementById('wishlist-content').style.display = 'none';
});

// ---------------- Close both dropdowns when clicking outside ----------------

document.addEventListener('click', function(event) {
    const wishlistContent = document.getElementById('wishlist-content');
    const userDropdown = document.getElementById("user-dropdown-content");

    // Close the wishlist if clicking outside of it
    if (wishlistContent.style.display === 'block' && !event.target.closest('#wishlist-btn')) {
        wishlistContent.style.display = 'none'; // Hide the wishlist
    }

    // Close the user dropdown if clicking outside of it
    if (userDropdown.classList.contains('show') && !event.target.closest('#user-icon-btn')) {
        userDropdown.classList.remove('show'); // Hide the user dropdown
    }
});