from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from decimal import Decimal

# Импортируем наши модули
from models import UserCreate, UserResponse, TransferRequest, TransferResponse
from storage import storage

# Создаем приложение FastAPI
app = FastAPI(
    title="Сервис управления списком пользователей и их балансом",
    description="REST API для управления пользователями и денежными переводами",
    version="1.0.0"
)


# Вспомогательная функция для получения пользователя или ошибки 404
def get_user_or_404(user_id: UUID) -> UserResponse:
    user = storage.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


# Роуты API
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):

    # Создать нового пользователя
    #
    # - name: Имя пользователя
    # - email: Email пользователя (должен быть уникальным)
    # - balance: Начальный баланс (не может быть отрицательным)

    try:
        from uuid import uuid4
        from models import UserResponse

        user_id = uuid4()
        user = UserResponse(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            balance=user_data.balance
        )
        storage.add_user(user)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/users", response_model=list[UserResponse])
async def get_users():

    # Получить список всех пользователей

    return storage.get_all_users()


@app.post("/transfer", response_model=TransferResponse)
async def make_transfer(transfer_data: TransferRequest):

    # Выполнить перевод между пользователями
    #
    # - from_user_id: ID пользователя-отправителя
    # - to_user_id: ID пользователя-получателя
    # - amount: Сумма перевода (должна быть положительной)

    # Проверка: нельзя переводить самому себе
    if transfer_data.from_user_id == transfer_data.to_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя переводить деньги самому себе"
        )

    # Получаем пользователей
    from_user = get_user_or_404(transfer_data.from_user_id)
    to_user = get_user_or_404(transfer_data.to_user_id)

    try:
        # Выполняем перевод
        updated_from_user = storage.update_user_balance(
            from_user.id,
            -transfer_data.amount
        )

        updated_to_user = storage.update_user_balance(
            to_user.id,
            transfer_data.amount
        )

        return TransferResponse(
            message="Перевод успешно выполнен",
            from_user_balance=updated_from_user.balance,
            to_user_balance=updated_to_user.balance
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Проверка работы сервера
@app.get("/")
async def root():
    return {"message": "Сервис управления пользователями работает!"}


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)