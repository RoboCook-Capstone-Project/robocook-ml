from fastapi import FastAPI
import uvicorn
import pickle

app = FastAPI()

@app.get('/')
def index() :
    return {'message': 'Hello world'}

@app.get('/test/for-you-page')
def fuse() :
    vectorizer = pickle.load(open('fusion_vectorizer.pkl'))
    return {'message': 'Hello world'}