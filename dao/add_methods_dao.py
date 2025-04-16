from typing import List

from dao.dao_models import UserDAO
from database import connection
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession

from sql_enums import GenderEnum, ProfessionEnum


@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add(session=session, **user_data)
    print(f'Добавлен новый пользователь с ID: {new_user.id}')
    return new_user.id


                              #Принимает
@connection                 #Список словарей
async def add_many(users_data: List[dict] , session: AsyncSession):
    new_users = await UserDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add_user_with_profile(session=session, user_data=user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

user_data_bob = {
    "username": "bob_smith",
    "email": "bob.smith@example.com",
    "password": "bobsecure456",
    "first_name": "Bob",
    "last_name": "Smith",
    "age": 25,
    "gender": GenderEnum.MALE,
    "profession": ProfessionEnum.DESIGNER,
    "interests": ["gaming", "photography", "traveling"],
    "contacts": {"phone": "+987654321", "email": "bob.smith@example.com"}
}

run(add_full_user(user_data=user_data_bob))