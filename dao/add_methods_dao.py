from typing import List

from dao.dao_models import UserDAO
from database import connection
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession


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
