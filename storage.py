from uuid import UUID
from decimal import Decimal
from typing import Dict, List, Optional
from models import UserResponse


class Storage:
    def __init__(self):
        self.users: Dict[UUID, UserResponse] = {}
        self.emails: set = set()

    def add_user(self, user: UserResponse) -> None:
        if user.email in self.emails:
            raise ValueError("Email уже существует")
        self.users[user.id] = user
        self.emails.add(user.email)

    def get_user(self, user_id: UUID) -> Optional[UserResponse]:
        return self.users.get(user_id)

    def get_all_users(self) -> List[UserResponse]:
        return list(self.users.values())

    def update_user_balance(self, user_id: UUID, amount: Decimal) -> UserResponse:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        new_balance = user.balance + amount
        if new_balance < 0:
            raise ValueError("Недостаточно средств")

        updated_user = UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            balance=new_balance
        )
        self.users[user_id] = updated_user
        return updated_user


# Глобальный экземпляр хранилища
storage = Storage()