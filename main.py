from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Roba un Huevo - Central Bot Hub",
    description="Servidor central receptor de datos enviados por bots escaneadores.",
    version="4.1.0"
)

# Base de datos temporal en memoria
servidores_db = {}

# Modelo de datos para validar la información
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
        "message": "API de Roba un Huevo Finder V4 activa."
    }

@app.get("/obtener_servidores", response_model=List[ServidorInfo])
def obtener_servidores_lista():
    """Ruta limpia de tipo GET para que tu interfaz de usuario lea la lista"""
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
    """Ruta de tipo POST para que los BOTS de la nube guarden los datos"""
    servidores_db[data.job_id] = {
        "jugadores": data.jugadores,
        "produccion": data.produccion,
        "ultima_actualizacion": data.ultima_actualizacion
    }
    return {"message": f"Servidor {data.job_id} registrado con éxito."}
