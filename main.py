from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# ========================================================
# 1. CONFIGURACIÓN DE CORS (PERMISOS DE CONEXIÓN EXTERNA)
# ========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos temporal en memoria
base_datos_servidores = {}

# Modelo de validación de datos
class ServidorRoblox(BaseModel):
    serverId: str
    playerCount: int
    eggCount: int
    specialEggs: int

# ========================================================
# 2. ENDPOINTS (RUTAS DE LA API)
# ========================================================

# Ruta Raíz: Evita el error 405 en pings automáticos
@app.get("/")
@app.head("/")
async def verificar_estado():
    return {
        "message": "API de Roba un Huevo Finder V4 activa.",
        "status": "online"
    }

# Endpoint 1 (POST): Recibe los datos del script de Roblox (Luau)
@app.post("/actualizar_servidor")
async def actualizar_servidor(data: ServidorRoblox):
    base_datos_servidores[data.serverId] = {
        "serverId": data.serverId,
        "playerCount": data.playerCount,
        "eggCount": data.eggCount,
        "specialEggs": data.specialEggs,
        "timestamp": time.time()
    }
    return {"status": "success", "message": "Datos de producción actualizados."}

# Endpoint 2 (GET): Envía los servidores recopilados a la aplicación de escritorio
@app.get("/obtener_servidores", response_model=List[dict])
async def obtener_servidores():
    lista_servidores = []
    tiempo_actual = time.time()
    
    for id_sv, datos in list(base_datos_servidores.items()):
        # Limpieza automática si el bot no reporta en 10 minutos (600 segundos)
        if tiempo_actual - datos["timestamp"] < 600:
            lista_servidores.append(datos)
        else:
            del base_datos_servidores[id_sv]
            
    return lista_servidores
