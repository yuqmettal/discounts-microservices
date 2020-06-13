import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/info")
async def health_info():
    return {"status": "UP"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
