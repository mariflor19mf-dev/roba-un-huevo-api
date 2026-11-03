from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos volátil en memoria
base_datos_servidores = {}

class ServidorRoblox(BaseModel):
    serverId: str
    playerCount: int
    eggCount: int
    specialEggs: int

# Evita el error 405 en pings automáticos de la raíz
@app.get("/")
@app.head("/")
async def verificar_estado():
    return {"status": "online", "proyecto": "Roba un Huevo Finder V4"}

# ENDPOINT 1: Recibe la transmisión del Script de Roblox (POST)
@app.post("/actualizar_servidor")
async def actualizar_servidor(data: ServidorRoblox):
    base_datos_servidores[data.serverId] = {
        "serverId": data.serverId,
        "playerCount": data.playerCount,
        "eggCount": data.eggCount,
        "specialEggs": data.specialEggs,
        "timestamp": time.time()
    }
    return {"status": "success"}

# ENDPOINT 2: Envía los datos guardados a la App de Escritorio (GET)
@app.get("/obtener_servidores", response_model=List[dict])
async def obtener_servidores():
    lista_servidores = []
    tiempo_actual = time.time()
    
    for id_sv, datos in list(base_datos_servidores.items()):
        # Si un bot no reporta en 5 minutos (300s), se borra el servidor de la lista
        if tiempo_actual - datos["timestamp"] < 300:
            lista_servidores.append(datos)
        else:
            del base_datos_servidores[id_sv]
            
    return lista_servidores
