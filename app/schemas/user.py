from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str = "customer"


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    role: str | None = None
    is_active: bool | None = None
