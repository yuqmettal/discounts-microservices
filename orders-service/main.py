import uvicorn
from fastapi import FastAPI
from py_eureka_client import eureka_client

import settings
from api.health import api_router as health_router
from api.v1 import api_router as v1_router


app = FastAPI(title="Orders service", openapi_url="/api/v1/openapi.json")

app.include_router(health_router)
app.include_router(v1_router, prefix='/api/v1')


eureka_client.init(
    eureka_server=settings.EUREKA_SERVER,
    app_name="orders-service",
    instance_port=int(settings.APP_PORT),
    instance_ip=settings.APP_HOST
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
