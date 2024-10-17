document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('product-search');
    const suggestionsList = document.getElementById('suggestions');

    function adjustSuggestionsWidth() {
        const inputWidth = searchInput.offsetWidth;
        suggestionsList.style.width = inputWidth + "px";
    }

    adjustSuggestionsWidth();
    
    window.addEventListener("resize", adjustSuggestionsWidth);

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length < 1) {
            suggestionsList.style.display = 'none'; // Hide suggestions when input is empty
            suggestionsList.innerHTML = ''; // Clear suggestions
            return;
        }

        // Optional: Show loading indication here

        fetch(`/products/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';  // Clear previous suggestions

                const uniqueNames = new Set(data);
                uniqueNames.forEach(productName => {
                    const p = document.createElement('p');
                    p.textContent = productName;

                    p.addEventListener('click', function() {
                        searchInput.value = productName;  // Set input value
                        suggestionsList.innerHTML = '';  // Clear suggestions
                        suggestionsList.style.display = 'none'; // Hide suggestions
                    });

                    suggestionsList.appendChild(p);
                });

                suggestionsList.style.display = uniqueNames.size > 0 ? 'block' : 'none';

                adjustSuggestionsWidth();
            })
            .catch(error => {
                console.error('Error:', error);
                // Optional: Display an error message to the user
            });
    });

    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.style.display = 'none';
        }
    });
});
