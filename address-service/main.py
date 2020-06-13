import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, models


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/info")
async def health_info():
    return {"status": "UP"}


@app.get("/api/v1/country")
async def get_all_countries(db: Session = Depends(get_db)):
    users = models.Country.query.all()
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
