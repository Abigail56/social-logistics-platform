from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.delivery import Delivery


class DeliveryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[Delivery]:
        statement = select(Delivery)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, delivery_id: int) -> Delivery | None:
        return await self.session.get(Delivery, delivery_id)

    async def create(self, delivery: Delivery) -> Delivery:
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery

    async def update(self, delivery: Delivery) -> Delivery:
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery
