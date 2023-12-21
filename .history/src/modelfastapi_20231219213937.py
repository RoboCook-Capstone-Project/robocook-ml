from fastapi import FastAPI
import uvicorn
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.get('/')
def index() :
    return {'message': 'Hello world'}

#bahan1, bahan2, top_n=5
@app.get('/test/fusion')
def fuse(bahan1:str, bahan2:str, top_n:int) :
    data = pd.read_csv
    vectorizer = pickle.load(open('fusion_vectorizer.pkl'))
    bahan_matrix = pickle.load(open('fusion_bahan_matrix.pkl'))
    bahan_gabung = f"{bahan1}--{bahan2}"
    bahan_gabung_vector = vectorizer.transform([bahan_gabung])

    # Calculate cosine similarity between the combined vector and all recipes
    resep_fusion = cosine_similarity(bahan_gabung_vector, bahan_matrix).flatten()
    resep_ouput = resep_fusion.argsort()[:-top_n-1:-1]

    return data.loc[resep_ouput, 'id'].tolist()