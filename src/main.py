
from reclameAqui import ReclameAqui
from instagram import Instagram
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reclameAqui")
def read_item():
    minerador = ReclameAqui()
    return minerador.minerar()

@app.get("/instagram")
def read_item():
    minerador = Instagram()
    return minerador.minerar()

