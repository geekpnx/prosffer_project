let wishList = [];
let totalPrice = 0;
let totalItems = 0; // For tracking total items


// Function to update quantity with a lower limit of 1
function updateQuantity(productId, amount) {
    const item = wishList.find(item => item.id === productId);
    if (item) {
        // Prevent decreasing quantity below 1
        if (item.quantity === 1 && amount === -1) {
            return; // Do nothing if quantity is 1 and the user tries to decrease it
        }
        item.quantity += amount;
        totalPrice += item.price * amount; // Update total price
        updateWishList();
    }
}



// Function to update the wishlist dropdown
function updateWishList() {
    const wishListItems = document.getElementById('wishlist-items');
    const totalPriceElement = document.getElementById('total-price-display');
    const itemCountElement = document.getElementById('wishlist-count'); // Element for showing the item count

    wishListItems.innerHTML = ''; // Clear existing items
    totalItems = 0; // Reset total items count

    wishList.forEach(item => {
        const li = document.createElement('li');

        // Create a product thumbnail image element
        const img = document.createElement('img');
        img.src = item.image;
        img.style.width = '50px'; // Set thumbnail size
        img.style.height = '50px';
        li.appendChild(img);

        // Add product name, price, and currency
        const text = document.createElement('span');
        text.textContent = `${item.name} - ${item.price * item.quantity} ${item.currency}`;
        li.appendChild(text);

        // Quantity controls
        const qtySpan = document.createElement('span');
        qtySpan.textContent = `Quantity: ${item.quantity}`;
        li.appendChild(qtySpan);

        const increaseBtn = document.createElement('button');
        increaseBtn.textContent = '+';
        increaseBtn.onclick = () => updateQuantity(item.id, 1);
        li.appendChild(increaseBtn);

        const decreaseBtn = document.createElement('button');
        decreaseBtn.textContent = '-';
        decreaseBtn.onclick = () => updateQuantity(item.id, -1);
        li.appendChild(decreaseBtn);

        // Remove button
        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.classList.add('remove-from-wishlist');
        removeButton.onclick = () => removeFromList(item.id);
        li.appendChild(removeButton);

        wishListItems.appendChild(li);

        totalItems += item.quantity; // Update total items count
    });

    totalPriceElement.textContent = `${totalPrice.toFixed(2)} €`; // Update total price
    document.getElementById('total-price').textContent = `${totalPrice.toFixed(2)} €`; // Update total price on the wishlist button

    // Update item count on wishlist icon
    itemCountElement.textContent = totalItems;
    itemCountElement.style.display = totalItems > 0 ? 'inline-block' : 'none'; // Show only if items are in the wishlist

}

// Function to add a product to the wishlist
function addToList(productId, productName, productPrice, productCurrency, productImage) {
    const existingItem = wishList.find(item => item.id === productId);
    if (!existingItem) {
        wishList.push({ id: productId, name: productName, price: productPrice, currency: productCurrency, image: productImage, quantity: 1 });
        totalPrice += productPrice; // Update total Price
    } else {
        existingItem.quantity++;
        totalPrice += productPrice; // Increase total price based on quantity
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
        totalPrice -= wishList[index].price * wishList[index].quantity; // Deduct price for all items
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

// Attach event listeners to add buttons
document.querySelectorAll('.add-to-wishlist').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        const productName = this.getAttribute('data-product-name');
        const productPrice = parseFloat(this.getAttribute('data-product-price'));
        const productCurrency = this.getAttribute('data-product-currency');
        const productImage = this.getAttribute('data-product-image'); // Add product image
        addToList(productId, productName, productPrice, productCurrency, productImage);
    });
});