import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from py_eureka_client import eureka_client

load_dotenv()

import settings
from database import engine, models
from api.v1 import api_router as v1_router
from api.health import api_router as health_router
from database.data.seed_data import seed_data


models.Base.metadata.create_all(bind=engine)

seed_data()

app = FastAPI(title="Address service", openapi_url="/address/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(v1_router, prefix='/api/v1')


eureka_client.init(
    eureka_server=settings.EUREKA_SERVER,
    app_name="address-service",
    instance_port=int(settings.APP_PORT),
    instance_ip=settings.APP_HOST
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
