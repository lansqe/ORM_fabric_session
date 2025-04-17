from dao.dao_models import UserDAO
from database import connection
from asyncio import run

from schemas import UsernameIDPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)


# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserPydantic.from_orm(i)
#     print(user_pydantic.dict())

rez =run(select_username_id())
for i in rez:
    rez = UsernameIDPydantic.from_orm(i)
    print(rez.dict())