from fastapi import APIRouter


router = APIRouter()


@router.get("/info")
async def health_info():
    return {"status": "UP"}
