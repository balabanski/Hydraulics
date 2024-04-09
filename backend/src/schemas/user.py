from typing import Optional

from pydantic import BaseModel, EmailStr, Field, root_validator

from backend.src.core.security import get_password_hash


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    hashed_password: Optional[str] = Field(alias="password")
    repeat_password: Optional[str]

    @root_validator
    def check_repeat_password(cls, values):
        pw1, pw2 = values.get("hashed_password"), values.get("repeat_password")
        print("pw1+++++++++", pw1, "\n", "pw2**********", pw2)
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        print("values__________", values)
        del values["repeat_password"]
        return values

    @root_validator
    def password_to_hash(cls, value):
        password = value.get("hashed_password")
        if password:
            hash_pas = get_password_hash(password)
            value["hashed_password"] = hash_pas
        print("value__________", value)

        return value


# Properties to receive via API on creation
class UserCreate(UserUpdate):
    email: EmailStr
    hashed_password: str = Field(alias="password")
    repeat_password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# crea = UserCreate(email='str@gmail.com', password='my_password', repeat_password='my_password')
# print('crea__________', crea)
