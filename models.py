from pydantic import BaseModel, EmailStr, condecimal
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional, List


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    balance: condecimal(ge=0) = Decimal('0.00')


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    balance: Decimal


class TransferRequest(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    amount: condecimal(gt=0)


class TransferResponse(BaseModel):
    message: str
    from_user_balance: Decimal
    to_user_balance: Decimal