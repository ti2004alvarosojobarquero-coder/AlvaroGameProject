import random
 
#la famosa lista de pokemons, primero creo una lista vacia global
personajesP = []
 
#------------------------------------------------------------#
#  CARGAR PERSONAJES
#  Lee personajes.txt y llena personajesP.
#  Formato de cada línea: nombre,hp,ataque,esquiva,imagen
#------------------------------------------------------------#
def cargar_personajes(archivo="personajes.txt"):
    global personajesP
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                nombre, hp, ataque, esquiva, imagen = linea.split(",")
                personajesP.append({
                    "nombre":  nombre,
                    "hp":      int(hp),
                    "ataque":  int(ataque),
                    "esquiva": float(esquiva),
                    "imagen":  imagen
                })
 
#------------------------------------------------------------#
#  CALCULAR DAÑO
#  Primero chequea si el defensor esquiva con su probabilidad.
#  Si esquiva retorna 0.
#  Si no: daño = ataque del atacante +- variacion aleatoria.
#  Minimo 1 de daño siempre.
#------------------------------------------------------------#
def calcular_daño(atacante, defensor):
    if random.random() < defensor.get("esquiva", 0):
        return 0
    variacion = random.randint(-5, 5)
    daño = atacante["ataque"] + variacion
    return max(1, daño)
 
#------------------------------------------------------------#
#  GENERAR EQUIPO ENEMIGO
#  Recibe el nivel (1-5) y el inventario del jugador.
#  El Hollow es solo el avatar del enemigo, NO pelea.
#  Se retorna su imagen por separado pa mostrarlo arriba.
#  El equipo son 3 pokemones de la lista de 15 que el
#  jugador NO tiene en su inventario (filtrado por nombre).
#  Retorna: (lista de 3 pokemones, path imagen del hollow)
#------------------------------------------------------------#
def generar_equipo_enemigo(nivel, inventario_jugador):
    # --- imagen del hollow pa mostrarlo como avatar enemigo ---
    hollow_imagenes = {
        1: "Hollow1.png",
        2: "Hollow2.png",
        3: "Hollow3.png",
        4: "Hollow4.png",
        5: "Hollow5.png",
    }
 
    # nombres que el jugador ya tiene pa filtrar
    nombres_jugador = {p["nombre"] for p in inventario_jugador}
 
    # 3 pokemones de la lista que el jugador NO tiene
    disponibles = [p for p in personajesP if p["nombre"] not in nombres_jugador]
 
    # fallback por si el jugador ya tiene casi todos
    if len(disponibles) < 3:
        disponibles = personajesP
 
    equipo = random.sample(disponibles, 3)
    return [dict(p) for p in equipo], hollow_imagenes[nivel]
 
#------------------------------------------------------------#
#  PUNTAJES  (estilo arcade: nombre → puntaje más alto)
#  Archivo puntajes.txt  →  una línea por jugador:
#      nombre,puntaje
#  guardar_puntaje() actualiza si el nuevo es mayor.
#  cargar_puntajes()  retorna lista ordenada de mayor a menor.
#------------------------------------------------------------#
ARCHIVO_PUNTAJES = "puntajes.txt"
 
def cargar_puntajes():
    """Retorna lista de dicts {nombre, puntaje} ordenada de mayor a menor."""
    tabla = {}
    try:
        with open(ARCHIVO_PUNTAJES, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    partes = linea.split(",")
                    if len(partes) == 2:
                        nombre  = partes[0].strip()
                        puntaje = int(partes[1].strip())
                        # guarda el mayor si el nombre aparece varias veces
                        if nombre not in tabla or puntaje > tabla[nombre]:
                            tabla[nombre] = puntaje
    except FileNotFoundError:
        pass
    return sorted(
        [{"nombre": n, "puntaje": p} for n, p in tabla.items()],
        key=lambda x: x["puntaje"],
        reverse=True
    )
 
def guardar_puntaje(nombre, puntaje):
    """
    Guarda o actualiza el puntaje del jugador.
    Si ya existe con un puntaje mayor, NO lo sobreescribe.
    Reescribe el archivo completo con la tabla actualizada.
    """
    tabla = {e["nombre"]: e["puntaje"] for e in cargar_puntajes()}
    if nombre not in tabla or puntaje > tabla[nombre]:
        tabla[nombre] = puntaje
    with open(ARCHIVO_PUNTAJES, "w", encoding="utf-8") as f:
        for n, p in tabla.items():
            f.write(f"{n},{p}\n")