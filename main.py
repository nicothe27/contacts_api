from fastapi import FastAPI
#Importamos managedb.py
from src.lib.managedb import ManageDB


app = FastAPI()
md = ManageDB()
@app.get("/")
async def root():
    return {"message":"Hello, FastAPI"}

@app.get("/api/contacts")
async def get_allcontacts():
    return md.read_contacts()