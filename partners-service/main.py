import uvicorn
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from py_eureka_client import eureka_client

load_dotenv()

import settings


app = FastAPI(title="Partners service")


eureka_client.init(
    eureka_server=settings.EUREKA_SERVER,
    app_name="partners-service",
    instance_port=int(settings.APP_PORT),
    instance_ip=settings.APP_HOST
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)