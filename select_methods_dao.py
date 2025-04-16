from dao.dao_models import UserDAO
from database import connection
from asyncio import run


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)

all_users = run(select_all_users())
for i in all_users:
    data = {'username': i.username, 'password': i.password, 'email': i.email}
    print(data)