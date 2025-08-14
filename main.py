from fastapi import FastAPI, HTTPException
#Importamos managedb.py
from src.lib.managedb import ManageDB


app = FastAPI()
md = ManageDB()
@app.get("/")
async def root():
    return {"message":"Hello, FastAPI"}

@app.get("/api/contacts")
async def get_allcontacts():
    return md.read_contacts() # Llamamos a la funcion read_contacts, usando la instancia de la clase ManageDB()


@app.get("/api/contacts/{id_contact}")
async def get_single_contact(id_contact:str):
    # Busca y retorna el contacto cuyo id coincide con el valor recibido en la URL.
    # Si no encuentra el contacto, no retorna nada !! (Falta agregar el mensaje de error)
    contacts = md.read_contacts()
    
    for contact in contacts:
        if contact["id"] == id_contact:
            return(contact) 
    raise HTTPException(status_code=404, detail="Contact not found")