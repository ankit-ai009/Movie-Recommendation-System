from flask import Flask, render_template, request, jsonify
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()  #  Load .env file

app = Flask(__name__)

#  Load models
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

#  Get API key securely
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

#  Fetch movie details
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos,credits,reviews"
    data = requests.get(url).json()

    # Poster
    poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else ""

    # Background
    backdrop = f"https://image.tmdb.org/t/p/original{data.get('backdrop_path')}" if data.get("backdrop_path") else ""

    # Genres
    genres = [g["name"] for g in data.get("genres", [])]

    # Trailer
    trailer = ""
    for vid in data.get("videos", {}).get("results", []):
        if vid["type"] == "Trailer":
            trailer = f"https://www.youtube.com/embed/{vid['key']}?autoplay=1&mute=1"
            break

    # Cast
    cast = []
    for actor in data.get("credits", {}).get("cast", [])[:8]:
        cast.append({
            "id": actor["id"],
            "name": actor["name"],
            "character": actor["character"],
            "image": f"https://image.tmdb.org/t/p/w200{actor['profile_path']}" if actor.get("profile_path") else ""
        })

    # Reviews
    reviews = []
    for r in data.get("reviews", {}).get("results", [])[:3]:
        reviews.append(r["content"])

    return {
        "title": data.get("title"),
        "overview": data.get("overview"),
        "rating": data.get("vote_average"),
        "release_date": data.get("release_date"),
        "poster": poster,
        "backdrop": backdrop,
        "genres": genres,
        "trailer": trailer,
        "cast": cast,
        "reviews": reviews
    }


#  Recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    results = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        results.append(fetch_movie_details(movie_id))

    return results


# Home page
@app.route('/')
def home():
    return render_template('home.html')


#  Recommendation API
@app.route('/recommend', methods=['POST'])
def recommend_api():
    movie_name = request.json['movie']
    return jsonify(recommend(movie_name))


#  Autocomplete
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify([])

    results = movies[movies['title'].str.contains(query, case=False)]
    return jsonify(results['title'].head(5).tolist())


#  Actor API
@app.route('/actor/<int:actor_id>')
def actor_details(actor_id):

    url = f"https://api.themoviedb.org/3/person/{actor_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()

    actor = {
        "name": data.get("name"),
        "birthday": data.get("birthday"),
        "place": data.get("place_of_birth"),
        "bio": data.get("biography"),
        "image": f"https://image.tmdb.org/t/p/w300{data.get('profile_path')}" if data.get("profile_path") else ""
    }

    return jsonify(actor)


#  Movie Details PAGE (ONLY ONE VERSION )
@app.route('/movie/<movie_name>')
def movie_details(movie_name):

    movie = movies[movies['title'] == movie_name]

    if movie.empty:
        return render_template("recommend.html", movie=None)

    movie_id = movie.iloc[0].movie_id
    details = fetch_movie_details(movie_id)

    return render_template("recommend.html", movie=details)


#  Run app
if __name__ == '__main__':
    app.run()
