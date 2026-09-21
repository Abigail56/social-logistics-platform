from pydantic import BaseModel, ConfigDict


class DeliveryBase(BaseModel):
    pickup_location: str
    destination: str
    package_details: str
    total_amount: float = 0.0


class DeliveryCreate(DeliveryBase):
    customer_id: int | None = None


class DeliveryUpdate(BaseModel):
    pickup_location: str | None = None
    destination: str | None = None
    package_details: str | None = None
    total_amount: float | None = None
    status: str | None = None


class DeliveryRead(DeliveryBase):
    id: int
    customer_id: int
    agent_id: int | None = None
    status: str = "REQUESTED"

    model_config = ConfigDict(from_attributes=True)
