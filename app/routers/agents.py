from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/")
async def list_agents():
    return []
