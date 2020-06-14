import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, models


models.Base.metadata.create_all(bind=engine)


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
    users = db.query(models.Country).all()
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
