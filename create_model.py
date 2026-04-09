import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

#  Load your movies data
movies = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies)

print("Movies loaded successfully ")

#  Check if 'tags' column exists
if 'tags' not in movies.columns:
    raise Exception(" 'tags' column not found in dataset")

#  Create vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

#  Fit and transform
vectors = vectorizer.fit_transform(movies['tags'])

print("Vectorization done ")

#  Save new files
pickle.dump(vectorizer, open('transform.pkl', 'wb'))
pickle.dump(vectors, open('nlp_model.pkl', 'wb'))

print(" New transform.pkl and nlp_model.pkl created successfully!")
