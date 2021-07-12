
import reclameAqui
import instagram
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reclameAqui")
def read_item():
    return reclameAqui.minerar()

@app.get("/instagram")
def read_item():
    return instagram.minerar()

