from fastapi import FastAPI
import uvicorn
import pickle

app = FastAPI()

@app.get('/')
def index() :
    return {'message': 'Hello world'}

@app.get('/test/for-you-page')
def recommend() :
    vectorizer = pickle.load
    return {'message': 'Hello world'}