import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import dill
from joblib import dump, load

# Masukin Data
data = pd.read_csv('../data/final/final_dataset.csv')
data['Ingredients'] = data['Ingredients'].fillna('') 

# Model Jarak Simpel
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('--'), token_pattern=None)
bahan_matrix = vectorizer.fit_transform(data['Ingredients'])

# Save
dump(vectorizer, 'fusion_vectorizer.joblib')
dump(bahan_matrix, 'fusion_bahan_matrix.joblib')

# Load
vectorizer = load('fusion_vectorizer.joblib')
bahan_matrix = load('fusion_bahan_matrix.joblib')

# Fungsi untuk Dipanggil
# INPUT: (string) bahan1, bahan2
# OUTPUT: list of ID
# Contoh input: 'chicken breast--crushed tomatoes--diced oninon' dan 'ground beef--red pepper'
def find_closest_recipes(bahan1, bahan2, top_n=5):
    # Gabung bahan resep input
    bahan_gabung = f"{bahan1}--{bahan2}"
    bahan_gabung_vector = vectorizer.transform([bahan_gabung])

    # Calculate cosine similarity between the combined vector and all recipes
    resep_fusion = cosine_similarity(bahan_gabung_vector, bahan_matrix).flatten()
    resep_ouput = resep_fusion.argsort()[:-top_n-1:-1]

    return data.loc[resep_ouput, 'id'].tolist()