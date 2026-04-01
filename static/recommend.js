function recommend() {

    let movie = document.getElementById("movieInput").value.trim();
    
    if (!movie) {
        alert("Please enter a movie name");
        return;
    }

    fetch("/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ movie: movie })
    })
    .then(res => res.json())
    .then(data => {
        let resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "";

        console.log("API response:", data); // 🔍 debug


        if (data.length === 0) {
            resultDiv.innerHTML = "<p>No recommendations found</p>";
            return;
        }

        data.forEach(movie => {

            let div = document.createElement("div");

            let poster = movie.poster
                ? movie.poster
                : "https://via.placeholder.com/150x220?text=No+Image";

            div.innerHTML = `
                <h3>${movie.title}</h3>
                <img src="${poster}" alt="poster">
                <p>⭐ ${movie.rating}</p>
            `;
             div.onclick = () => {
        window.location.href = `/movie/${encodeURIComponent(movie.title)}`;
    };

            resultDiv.appendChild(div);
        });
    })
    .catch(err => {
        console.error("Recommend error:", err);
    });
}