from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.delivery import Delivery
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.delivery import DeliveryCreate, DeliveryRead, DeliveryUpdate
from app.services.delivery_service import DeliveryService

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/", response_model=list[DeliveryRead])
async def list_deliveries(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = DeliveryRepository(session)
    return await repo.list()


@router.post("/", response_model=DeliveryRead)
async def create_delivery(
    payload: DeliveryCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = DeliveryRepository(session)
    delivery = Delivery(
        customer_id=payload.customer_id or 1,
        pickup_location=payload.pickup_location,
        destination=payload.destination,
        package_details=payload.package_details,
        total_amount=payload.total_amount,
        status="REQUESTED",
    )
    return await repo.create(delivery)


@router.patch("/{delivery_id}", response_model=DeliveryRead)
async def update_delivery(
    delivery_id: int,
    payload: DeliveryUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = DeliveryRepository(session)
    delivery = await repo.get(delivery_id)
    if delivery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found",
        )

    current_status = delivery.status
    if payload.status and not DeliveryService.can_update_status(
        current_status,
        payload.status,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid delivery status transition",
        )

    if payload.pickup_location is not None:
        delivery.pickup_location = payload.pickup_location
    if payload.destination is not None:
        delivery.destination = payload.destination
    if payload.package_details is not None:
        delivery.package_details = payload.package_details
    if payload.total_amount is not None:
        delivery.total_amount = payload.total_amount
    if payload.status is not None:
        delivery.status = payload.status

    return await repo.update(delivery)
