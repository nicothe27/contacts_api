import pathlib
import json


# Definimos una variable privada para almacenar los contactos
class ManageDB:
    #Con pathlib.Path convertimos la ruta __file__ en un objeto
    #Usamos .parent.parent para ir subir dos niveles desde managed.py (lib a src y de src a app)
    #Evitamos poner la ruta absoluta pathlib.Path("c:/Users/User/Desktop/apiRest/app/src/db/dbContacts.json")
    __address_file = pathlib.Path(__file__).parent.parent / "db" / "dbContacts.json"
    
    def read_contacts(self):
        with open(self.__address_file, "r") as data:
            return json.loads(data.read()) #json.load para convertirlo a json    
        