function saveWishListToDatabase() {
    $.ajax({
        url: saveWishlistUrl,  // Use the dynamically generated URL from Django
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
        },
        data: JSON.stringify(wishList),  // Send the wishlist data as JSON
        contentType: 'application/json',
        success: function(response) {
            console.log("Wishlist saved successfully:", response);
            alert("Wishlist has been saved to your profile!");  // Optional user feedback
        },
        error: function(xhr, status, error) {
            console.error("Error saving wishlist:", error);
            alert("There was an error saving your wishlist. Please try again.");  // Optional user feedback
        }
    });
}