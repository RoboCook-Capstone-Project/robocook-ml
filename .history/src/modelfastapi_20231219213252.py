from fastapi import FastAPI
import uvicorn
import pickle

app = FastAPI()

@app.get('/')
def index() :
    return {'message': 'Hello world'}

#bahan1, bahan2, top_n=5
@app.get('/test/fusion')
def fuse() :
    vectorizer = pickle.load(open('fusion_vectorizer.pkl'))
    return {'message': 'Hello world'}