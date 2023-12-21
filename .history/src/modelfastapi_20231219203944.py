from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def index() :
    return {'message': 'Hello world'}

@app.get('/test/')
def index() :
    return {'message': 'Hello world'}