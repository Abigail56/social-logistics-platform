from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/")
async def receive_webhook():
    return {"status": "ok"}
