from pydantic import BaseModel, ConfigDict


class AgentBase(BaseModel):
    is_available: bool = True
    rating: float = 0.0


class AgentCreate(AgentBase):
    user_id: int


class AgentRead(AgentBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
