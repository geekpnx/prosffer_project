document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('product-search');
    const suggestionsList = document.getElementById('suggestions');

    // Function to match suggestions width with input width
    function adjustSuggestionsWidth() {
        const inputWidth = searchInput.offsetWidth;
        suggestionsList.style.width = inputWidth + "px";
    }

    // Adjust on page load
    adjustSuggestionsWidth();

    // Adjust on window resize
    window.addEventListener("resize", function() {
        adjustSuggestionsWidth();
    });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length < 1) {
            suggestionsList.style.display = 'none'; // Hide suggestions when input is empty
            suggestionsList.innerHTML = ''; // Clear suggestions
            return;
        }

        fetch(`/products/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';  // Clear previous suggestions

                // Use a Set to track unique product names
                const uniqueNames = new Set(data);

                uniqueNames.forEach(productName => {
                    const p = document.createElement('p');
                    p.textContent = productName;

                    // Add click event to select the suggestion
                    p.addEventListener('click', function() {
                        searchInput.value = productName;  // Set the input value to the selected suggestion
                        suggestionsList.innerHTML = '';  // Clear the suggestions after selection
                        suggestionsList.style.display = 'none'; // Hide suggestions box
                    });

                    suggestionsList.appendChild(p);
                });

                // Show suggestions box when there are results
                if (uniqueNames.size > 0) {
                    suggestionsList.style.display = 'block';
                } else {
                    suggestionsList.style.display = 'none';
                }

                // Adjust the width of suggestions after adding suggestions
                adjustSuggestionsWidth();
            })
            .catch(error => console.error('Error:', error));
    });

    // Hide the suggestions when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.style.display = 'none';
        }
    });
});