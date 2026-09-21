from fastapi import FastAPI

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.timing import TimingMiddleware
from app.routers.agents import router as agents_router
from app.routers.auth import router as auth_router
from app.routers.deliveries import router as deliveries_router
from app.routers.payments import router as payments_router
from app.routers.users import router as users_router
from app.routers.webhooks import router as webhooks_router

app = FastAPI(
    title="Social Logistics Platform",
    version="1.0.0",
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(agents_router)
app.include_router(deliveries_router)
app.include_router(payments_router)
app.include_router(webhooks_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "social-logistics-api",
    }
