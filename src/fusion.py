import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Masukin Data
data = pd.read_csv('final_dataset.csv')
data['Ingredients'] = data['Ingredients'].fillna('') 

# Model Jarak Simpel
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('--'), token_pattern=None)
bahan_matrix = vectorizer.fit_transform(data['Ingredients'])

# Fungsi untuk Dipanggil
# INPUT: List(strings) bahan1, bahan2
def fusion_recipes(id_1, id_2, top_n=5):
    # Gabung bahan dari resep input
    resep_input = [id_1, id_2]
    
    # UBAH JADI AMBIL INGREDIENTS DARI DATABASE
    #              BAGIAN YANG INI
    resep_gabung = data.loc[resep_input, 'Ingredients'].str.cat(sep='--')
    
    resep_gabung_vector = vectorizer.transform([resep_gabung])

    # Cari top 5 resep yang paling mirip
    resep_fusion = cosine_similarity(resep_gabung_vector, bahan_matrix).flatten()
    resep_fusion = resep_fusion.argsort()[:-top_n-1:-1]

    return data.loc[resep_fusion, 'id'].tolist()