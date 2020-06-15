from api.v1 import api_router as v1_router
from api.health import api_router as health_router
import settings
import uvicorn
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from py_eureka_client import eureka_client

from database.data.seed_data import seed_data
from database import models, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

seed_data()

app = FastAPI(title="Partners service", openapi_url="/api/v1/openapi.json")

app.include_router(health_router)
app.include_router(v1_router, prefix='/api/v1')


eureka_client.init(
    eureka_server=settings.EUREKA_SERVER,
    app_name="partners-service",
    instance_port=int(settings.APP_PORT),
    instance_ip=settings.APP_HOST
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
