from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Roba un Huevo - Central Bot Hub",
    description="Servidor central receptor de datos enviados por bots exploradores",
    version="4.1.0"
)

servidores_activos = {}

class ReporteBotIn(BaseModel):
    job_id: str
    egg_name: str
    rarity: str
    production_bps: float
    multiplier: Optional[float] = 1.0
    players: str = "1/7"

class ReporteFinderOut(BaseModel):
    job_id: str
    egg_name: str
    rarity: str
    production_bps: float
    multiplier: Optional[float]
    players: str
    last_seen_seconds: int

@app.post("/bot/reportar", status_code=status.HTTP_201_CREATED)
def reporte_desde_bot(data: ReporteBotIn):
    if data.production_bps < 5.0:
        raise HTTPException(status_code=400, detail="Producción insuficiente.")
    servidores_activos[data.job_id] = {
        **data.dict(),
        "timestamp": datetime.now(timezone.utc)
    }
    return {"status": "success"}

@app.get("/finder/actualizar", response_model=List[ReporteFinderOut])
def enviar_a_finder(min_prod: float = 5.0):
    ahora = datetime.now(timezone.utc)
    lista_limpia = []
    for job_id, info in list(servidores_activos.items()):
        segundos = int((ahora - info["timestamp"]).total_seconds())
        if segundos > 900:
            servidores_activos.pop(job_id, None)
            continue
        if info["production_bps"] >= min_prod:
            lista_limpia.append(ReporteFinderOut(
                job_id=info["job_id"],
                egg_name=info["egg_name"],
                rarity=info["rarity"],
                production_bps=info["production_bps"],
                multiplier=info["multiplier"],
                players=info["players"],
                last_seen_seconds=segundos
            ))
    lista_limpia.sort(key=lambda x: -x.production_bps)
    return lista_limpia
