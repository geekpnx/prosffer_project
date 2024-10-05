var updateBtns = document.getElementsByClassName('update-wishlist');

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'action:', action);

    console.log('USER:', user);
    if (user === 'AnonymousUser') {
      console.log('User is Not logged in');
    } else {
      updateUserWishlist(productId, action);
    }
  });
}

function updateUserWishlist(productId, action) {
  console.log('User is logged in, sending data..');

  var url = '/wishlist/update_item/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'productId': productId, 'action': action })
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log('data:', data);

      // Update the cart total in the navbar
      document.getElementById('cart-total').innerText = data.wishlist_items;

      // Update the quantity displayed in the wishlist
      var quantityElement = document.querySelector(`.quantity[data-product='${productId}']`);

      if (quantityElement) {
        // Update displayed quantity
        var newQuantity = action === 'add' ?
          parseInt(quantityElement.innerText) + 1 :
          parseInt(quantityElement.innerText) - 1;

        // Prevent negative quantity
        newQuantity = Math.max(newQuantity, 0);
        quantityElement.innerText = newQuantity;

        // Update the total for this product (price * quantity)
        var priceElement = document.querySelector(`.price[data-product='${productId}']`);
        var totalElement = document.querySelector(`.total[data-product='${productId}']`);
        
        if (priceElement && totalElement) {
          var productPrice = parseFloat(priceElement.innerText.replace('€', ''));
          var newTotal = productPrice * newQuantity;
          totalElement.innerText = '€' + newTotal.toFixed(2);
        }

        // Optionally, if quantity is 0, remove the item from the DOM or notify the user
        if (newQuantity === 0) {
          var itemRow = quantityElement.closest('.cart-row');
          if (itemRow) {
            itemRow.remove();
          }
        }

        // Update the overall wishlist total after each change
        updateWishlistTotal();

        updateWishlistItemCount();
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to update the overall wishlist total
function updateWishlistTotal() {
  var totalElements = document.querySelectorAll('.total'); // Select all individual product totals
  var wishlistTotal = 0;

  totalElements.forEach(function(totalElement) {
    var productTotal = parseFloat(totalElement.innerText.replace('€', ''));
    wishlistTotal += productTotal;
  });

  // Update the grand total element in the DOM
  document.getElementById('wishlist-total').innerText = '€' + wishlistTotal.toFixed(2);
}
function updateWishlistItemCount() {
  var quantityElements = document.querySelectorAll('.quantity[data-product]'); // Select all quantity elements
  var totalItems = 0;

  quantityElements.forEach(function (quantityElement) {
    var itemQuantity = parseInt(quantityElement.innerText);
    totalItems += itemQuantity;
  });

  // Update the total items count element in the DOM
  document.getElementById('item-total').innerText = totalItems;
}
