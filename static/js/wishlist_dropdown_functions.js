// Now you can make AJAX requests without needing to set the token each time

let wishList = [];
let totalPrice = 0;

// Function to get CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up the CSRF token in AJAX requests
const csrfToken = getCookie('csrftoken');

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrfToken
    }
});


// Function to update the wishlist dropdown
function updateWishList() {
    const wishListItems = document.getElementById('wishlist-items');
    const totalPriceElement = document.getElementById('total-price-display');

    wishListItems.innerHTML = ''; // Clear existing items
    wishList.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.price} ${item.currency}`;
        const removeButton = document.createElement('button');
        removeButton.textContent = 'X';
        removeButton.classList.add('remove-from-wishlist');
        removeButton.onclick = () => removeFromList(item.id);
        li.appendChild(removeButton);
        wishListItems.appendChild(li);
    });

    totalPriceElement.textContent = `${totalPrice.toFixed(2)} €`; // Update total price
    document.getElementById('total-price').textContent = `${totalPrice.toFixed(2)} €`; // Update the total price on the wishlist button
}

// Function to add a product to the wishlist
function addToList(productId, productName, productPrice, productCurrency) {
    const existingItem = wishList.find(item => item.id === productId);
    if (!existingItem) {
        wishList.push({ id: productId, name: productName, price: productPrice, currency: productCurrency });
        totalPrice += productPrice; // Update total Price
        console.log(`Added ${productName} - ${productPrice} ${productCurrency}`); // Debugging output
    } else {
        console.log(`${productName} is already in the wishlist.`); // Debugging output
    }

    updateWishList();
    // AJAX call to the server
    $.ajax({
        url: `/wishlist/add/${productId}/`, // URL to add the product to the wishlist
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is included
        },
        success: function(response) {
            console.log("Product added to wishlist:", response);
        },
        error: function(xhr, status, error) {
            console.error("Error adding to wishlist:", error);
        }
    });
}

// Function to remove a product from the wishlist
function removeFromList(productId) {
    const index = wishList.findIndex(item => item.id === productId);
    if (index > -1) {
        totalPrice -= wishList[index].price; // Deduct price
        wishList.splice(index, 1); // Remove item
    }
    updateWishList();
    // AJAX call to the server
    $.ajax({
        url: `/wishlist/remove/${productId}/`, // URL to remove the product from the wishlist
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is included
        },
        success: function(response) {
            console.log("Product removed from wishlist:", response);
        },
        error: function(xhr, status, error) {
            console.error("Error removing from wishlist:", error);
        }
    });
}

// Function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Attach event listeners to add buttons
document.querySelectorAll('.add-to-wishlist').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        const productName = this.getAttribute('data-product-name');
        const productPrice = parseFloat(this.getAttribute('data-product-price'));
        const productCurrency = this.getAttribute('data-product-currency');
        addToList(productId, productName, productPrice, productCurrency);
    });
});

