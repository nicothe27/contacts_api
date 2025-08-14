from fastapi import FastAPI, HTTPException
## uuid para generar id's unicos
from uuid import uuid4 as uuid
## Usamos basemodel de pydantic para deinir modelos de datos y validarlos con los datos recibidos en las peticiones de la API
from pydantic import BaseModel

#Importamos managedb.py
from src.lib.managedb import ManageDB


#Definimos como debe ser un contacto (heredando BaseModel de pydantic. Si no se envía el id, se genera automaticamente usando uuid())
class ContactModel(BaseModel):
    id: str = str(uuid())
    name: str 
    phone: str

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
    raise HTTPException(status_code=404, detail="Contact not found") # Importo HTTPException para manejar error de contacto no encontrado

@app.post("/api/contacts")
async def add_contact(new_contact: ContactModel):
    contacts = md.read_contacts() #Lee los contactos
    new_contact = new_contact.dict() #Convierte el modelo de pydantic a diccionario para poderlo almacenar
    contacts.append(new_contact) #Agrega el nuevo contacto a la lista existente   
    md.write_contacts(contacts) #Guarda la lista actualizada en el archivo json
    return {
        "Success":"True",
        "message":"New contact added"
    }
    
@app.put("/api/contacts")
# Recibe el id del contacto a actualizar, y los nuevos datos del contacto
async def update_contact(id_contact: str, new_contact: ContactModel):
    contacts = md.read_contacts() #Leemos la lista actual de contactos
    
    for index, contact in enumerate(contacts): #El enumerate() recorre la lista contacts y en cada vuelta te da el index y el contacto
        if contact["id"] == id_contact:
            contacts[index] = new_contact.dict() #Si encuentra el id, lo reemplaza por el nuevo (convertido a diccionario)
            
            if new_contact.name == "":
                contacts[index]["name"] = contact["name"] #Condicion para conservar el nombre si el nuevo está vacío
                
            if new_contact.phone == "":
                contacts[index]["phone"] = contact["phone"] #Condicion para conservar el numero si el nuevo está vacío
            
            md.write_contacts(contacts) #Guardamos la lista actualizada en el json
            
            return{
                "succes":"true",
                "message":"Contact Updated"
            } # Mensaje de exito default
                    
    raise HTTPException(status_code=404, detail="Contacto no encontrado") #Retornamos un error con HTTPException
        
    