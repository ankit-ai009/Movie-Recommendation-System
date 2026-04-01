let input = document.getElementById("movieInput");
let suggestionBox = document.getElementById("suggestions");

// ⏳ debounce to reduce API calls
let timeout = null;

input.addEventListener("keyup", function () {

    clearTimeout(timeout);

    timeout = setTimeout(() => {
        let query = input.value.trim();

        // ❌ stop if empty
        if (query.length === 0) {
            suggestionBox.innerHTML = "";
            return;
        }

        fetch('/autocomplete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        })
        .then(res => res.json())
        .then(data => {

            suggestionBox.innerHTML = "";

            if (data.length === 0) {
                suggestionBox.innerHTML = "<li>No results</li>";
                return;
            }

            data.forEach(movie => {
                let li = document.createElement("li");
                li.innerText = movie;

                li.onclick = () => {
                    input.value = movie;
                    suggestionBox.innerHTML = "";
                };

                suggestionBox.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Autocomplete error:", err);
        });

    }, 300); // delay 300ms
});


// 🔥 Hide suggestions when clicking outside
document.addEventListener("click", function(e) {
    if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
        suggestionBox.innerHTML = "";
    }
});