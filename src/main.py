
from reclameAqui import ReclameAqui
from instagram import Instagram
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reclameAqui/")
def read_item(empresa: str):
    minerador = ReclameAqui()
    return minerador.minerarEmpresa(empresa)


@app.get("/reclameAqui/rankings")
def read_item():
    minerador = ReclameAqui()
    return minerador.minerar()

