import uvicorn
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

load_dotenv()

from database import engine, models
from api.v1 import api_router as v1_router
from api.health import api_router as health_router
from database.data.seed_data import seed_data


models.Base.metadata.create_all(bind=engine)

seed_data()

app = FastAPI(title="Address service", openapi_url="/api/v1/openapi.json")

app.include_router(health_router)
app.include_router(v1_router, prefix='/api/v1')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
