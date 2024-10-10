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
    const wishListItems = document.querySelector('#wishlist-items tbody');
    const totalPriceElement = document.getElementById('total-price-display');
    const itemCountElement = document.getElementById('wishlist-count');

    wishListItems.innerHTML = ''; // Clear existing items
    totalItems = 0; // Reset total items count

    wishList.forEach(item => {
        const row = document.createElement('tr');

        // Create product image cell
        const imgCell = document.createElement('td');
        const img = document.createElement('img');
        img.src = item.image;
        img.style.width = '50px'; // Thumbnail size
        img.style.height = '50px';
        imgCell.appendChild(img);
        row.appendChild(imgCell);

        // Store name
        const storeCell = document.createElement('td');
        storeCell.textContent = item.storeName; // Assuming you have a store property
        row.appendChild(storeCell);

        // Product name
        const nameCell = document.createElement('td');
        nameCell.textContent = item.name;
        row.appendChild(nameCell);

        // Quantity cell
        const qtyCell = document.createElement('td');
        qtyCell.textContent = item.quantity;
        row.appendChild(qtyCell);

        // Price cell
        const priceCell = document.createElement('td');
        priceCell.textContent = `${(item.price * item.quantity).toFixed(2)} ${item.currency}`;
        row.appendChild(priceCell);

        // Actions cell
        const actionsCell = document.createElement('td');
        
        // Increase button
        const increaseBtn = document.createElement('button');
        increaseBtn.textContent = '+';
        increaseBtn.onclick = () => updateQuantity(item.id, 1);
        actionsCell.appendChild(increaseBtn);

        // Decrease button
        const decreaseBtn = document.createElement('button');
        decreaseBtn.textContent = '-';
        decreaseBtn.onclick = () => updateQuantity(item.id, -1);
        actionsCell.appendChild(decreaseBtn);

        // Remove button
        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.classList.add('remove-from-wishlist');
        removeButton.onclick = () => removeFromList(item.id);
        actionsCell.appendChild(removeButton);

        row.appendChild(actionsCell);
        wishListItems.appendChild(row);

        totalItems += item.quantity; // Update total items count
    });

    totalPriceElement.textContent = `${totalPrice.toFixed(2)} €`; // Update total price
    document.getElementById('total-price').textContent = `${totalPrice.toFixed(2)} €`;

    // Update item count on wishlist icon
    itemCountElement.textContent = totalItems;
    itemCountElement.style.display = totalItems > 0 ? 'inline-block' : 'none'; // Show only if items are in the wishlist
}

// Function to add a product to the wishlist
function addToList(productId, storeName, productName, productPrice, productCurrency, productImage) {
    const existingItem = wishList.find(item => item.id === productId);
    if (!existingItem) {
        wishList.push({ 
            id: productId, 
            storeName,
            name: productName, 
            price: productPrice, 
            currency: productCurrency, 
            image: productImage, 
            quantity: 1 });

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
        const storeName = this.getAttribute('data-store-name');
        const productName = this.getAttribute('data-product-name');
        const productPrice = parseFloat(this.getAttribute('data-product-price'));
        const productCurrency = this.getAttribute('data-product-currency');
        const productImage = this.getAttribute('data-product-image'); // Add product image
        addToList(productId, storeName, productName, productPrice, productCurrency, productImage);
    });
});