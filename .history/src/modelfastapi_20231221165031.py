from fastapi import FastAPI
import uvicorn
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

data = pd.read_csv('C:\Users\Debra Mazaya\Desktop\Semester 7\Bangkit Machine Learning\Capstone\robocook-ml\src\modelfastapi.py')

@app.get('/')
def index() :
    return data.head().to_dict(orient='records')

#API Endpoint for Fusion Model
@app.post('/api/recipe-model/fusion')
def fuse(bahan1:str, bahan2:str) :
    top_n = 5
    data['Ingredients'] = data['Ingredients'].fillna('') 

    # Model Jarak Simpel
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split('--'), token_pattern=None)
    bahan_matrix = vectorizer.fit_transform(data['Ingredients'])
    
    # Gabung bahan resep input
    bahan_gabung = f"{bahan1}--{bahan2}"
    bahan_gabung_vector = vectorizer.transform([bahan_gabung])

    # Calculate cosine similarity between the combined vector and all recipes
    resep_fusion = cosine_similarity(bahan_gabung_vector, bahan_matrix).flatten()
    resep_ouput = resep_fusion.argsort()[:-top_n-1:-1]

    return data.loc[resep_ouput, 'id'].tolist()

#API Endpoint for For You Page Recommendation Model
#Note : Setiap page akan mengeluarkan 20 resep, jadi ini bakal dijalanin di setiap page
@app.get('/api/recipe-model/fyp')
def recommend(recipe_id:int, start:int, end:int) :
    n = 100

    data['Ingredients'] = data['Ingredients'].fillna('')

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Ingredients'])

    knn_model = NearestNeighbors(algorithm='auto', metric='cosine').fit(tfidf_matrix)

    # Get ID recommendations
    # Returns recommended recipe id from index start to end
    idx = data[data['id'] == recipe_id].index[0]
    recipe_tfidf_vector = tfidf_matrix[idx]
    _, indices = knn_model.kneighbors(recipe_tfidf_vector, n_neighbors=n+1)
    similar_recipe_indices = indices.flatten()[1:]
    # Starting index at 1
    similar_recipe_id = data.iloc[similar_recipe_indices]['id'][start-1:end]
    return similar_recipe_id.tolist()