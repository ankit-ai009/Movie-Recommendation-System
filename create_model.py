# create_model.py

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("🚀 Starting model creation...")

# 🔹 STEP 1: Load RAW dataset (IMPORTANT)
# 👉 Make sure this file exists in your repo
movies = pd.read_csv('tmdb_5000_movies.csv')

print("✅ CSV loaded successfully")

# 🔹 STEP 2: Select useful columns
movies = movies[['id', 'title', 'overview']]
movies.dropna(inplace=True)

# 🔹 STEP 3: Create 'tags' column (simple version)
movies['tags'] = movies['overview']

print("✅ Tags created")

# 🔹 STEP 4: Vectorization
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(movies['tags'])

print("✅ Vectorization done")

# 🔹 STEP 5: Similarity matrix (OPTIONAL but useful)
similarity = cosine_similarity(vectors)

print("✅ Similarity matrix created")

# 🔹 STEP 6: Save files
pickle.dump(movies.to_dict(), open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
pickle.dump(vectorizer, open('transform.pkl', 'wb'))

print("🎉 All model files created successfully!")
