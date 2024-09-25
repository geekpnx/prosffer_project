document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('product-search');
    const suggestionsList = document.getElementById('suggestions');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length < 1) {
            suggestionsList.innerHTML = '';  // Clear suggestions if input is empty
            return;
        }

        fetch(`/products/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';  // Clear previous suggestions

                // Use a Set to track unique product names
                const uniqueNames = new Set(data);

                uniqueNames.forEach(productName => {
                    const li = document.createElement('li');
                    li.textContent = productName;

                    // Add click event to select the suggestion
                    li.addEventListener('click', function() {
                        searchInput.value = productName;  // Set the input value to the selected suggestion
                        suggestionsList.innerHTML = '';  // Clear the suggestions after selection
                    });

                    suggestionsList.appendChild(li);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});