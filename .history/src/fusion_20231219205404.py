import pandas as pd
import scikit-learn as sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Masukin Data
data = pd.read_csv('../data/final/final_dataset.csv')
data['Ingredients'] = data['Ingredients'].fillna('') 

# Model Jarak Simpel
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('--'), token_pattern=None)
bahan_matrix = vectorizer.fit_transform(data['Ingredients'])

pickle_vectorizer = open('fusion_vectorizer.pkl', 'wb')
pickle.dump(vectorizer, pickle_vectorizer)
pickle_vectorizer.close()

pickle_matrix = open('fusion_bahan_matrix.pkl', 'wb')
pickle.dump(bahan_matrix, pickle_matrix)
pickle_vectorizer.close()

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