from fastapi import FastAPI


app = FastAPI()


@app.get("/info")
async def health_info():
    return {"status": "UP"}
