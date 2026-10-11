from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import medicion, sensor, sensor_magnitud
from app.mqtt.client import start_mqtt, stop_mqtt


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_mqtt()
    yield
    # Shutdown
    stop_mqtt()


app = FastAPI(
    title="API IoT AQ-003",
    description="API para adquisicion, validacion y consulta de datos IoT",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(sensor.router)
app.include_router(sensor_magnitud.router)
app.include_router(medicion.router)


@app.get("/", tags=["root"])
def root():
    return {"mensaje": "API IoT AQ-003 funcionando"}