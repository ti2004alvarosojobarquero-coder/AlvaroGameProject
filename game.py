#la famosa lista de pokemons, primero creo una lista vacia global
personajesP = []

def cargar_personajes(archivo="personajes.txt"): # esto para poder llamarla vacia y que busque el archivo
    # f es el archivo abierto,  with open lo abre, "r" es para read, encoding para caracteres
    with open(archivo, "r", encoding="utf-8") as f: 
        for linea in f:
            linea = linea.strip() #eliminar espacios y \n
            if linea: #si la linea no esta vacia
                nombre, hp, ataque, critico = linea.split(",") # partir el string y guardar cada dato en una varable
                #____________--------------________________________---------------------___________________________#
                #---------------------------------diccionario para la lista----------------------------------------#
                personajesP.append({
                    "nombre": nombre,
                    "hp": int(hp),
                    "ataque": int(ataque),
                    "critico": float(critico)
                })
puntaje = 0 
def puntaje():
    puntaje = 2
    return puntaje + 1

def restar_puntaje():
    return puntaje - 1

    