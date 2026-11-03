from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

app = FastAPI(
    title="Roba un Huevo - Central Bot Hub",
    description="Servidor central receptor de datos enviados por bots escaneadores.",
    version="4.1.0"
)

# Base de datos temporal en memoria
servidores_db = {}

# Modelo de datos que esperan recibir los bots
class ServidorInfo(BaseModel):
    job_id: str
    jugadores: str = "0/0"
    produccion: str = "Desconocida"
    ultima_actualizacion: str = "Justo ahora"

@app.get("/")
def home():
    """Verificación de estado de la API"""
    return {
        "status": "online",
        "message": "API de Roba un Huevo Finder V4 activa y funcionando correctamente."
    }

# ESTA ES LA RUTA QUE BUSCA TU PROGRAMA LOCAL AL DARLE AL BOTÓN
@app.get("/actualizar_servidores", response_model=List[ServidorInfo])
def obtener_servidores_get():
    """Ruta para que tu interfaz de usuario lea la lista de servidores"""
    lista = []
    for j_id, info in servidores_db.items():
        lista.append(ServidorInfo(
            job_id=j_id,
            jugadores=info["jugadores"],
            produccion=info["produccion"],
            ultima_actualizacion=info["ultima_actualizacion"]
        ))
    return lista

@app.post("/actualizar_servidores")
def registrar_o_actualizar_servidor(data: ServidorInfo):
    """Ruta para que los BOTS de la nube guarden los datos recogidos"""
    servidores_db[data.job_id] = {
        "jugadores": data.jugadores,
        "produccion": data.produccion,
        "ultima_actualizacion": data.ultima_actualizacion
    }
    return {"message": f"Servidor {data.job_id} registrado/actualizado con éxito."}
