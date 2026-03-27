from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("/")
async def get_agents():
    return {"agents": [], "message": "Agents list"}

@router.get("/test")
async def test():
    return {"message": "Agents router is working"}
