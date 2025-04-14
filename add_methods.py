from sqlalchemy.ext.asyncio import AsyncSession
from database import connection
from asyncio import run
from models import User, Profile
from sql_enums import GenderEnum, ProfessionEnum


@connection
async def create_new_user(
        username:str,
        email: str,
        password: str,
        session: AsyncSession
) -> int:
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id


# new_user_id = run(create_new_user(username="Bovarina", email="ext@ext.com", password="asdasd"))
#
# print(f"Новый пользователь с идентификатором {new_user_id} создан")

# @connection
# async def get_user_by_id_example_2(username: str, email: str, password: str,
#                                    first_name: str,
#                                    last_name: str | None,
#                                    age: str | None,
#                                    gender: GenderEnum,
#                                    profession: ProfessionEnum | None,
#                                    interests: list | None,
#                                    contacts: dict | None,
#                                    session: AsyncSession) -> dict[str, int]:
#     user = User(username=username, email=email, password=password)
#     session.add(user)
#     await session.commit()
#
#     profile = Profile(
#         user_id=user.id,
#         first_name=first_name,
#         last_name=last_name,
#         age=age,
#         gender=gender,
#         profession=profession,
#         interests=interests,
#         contacts=contacts)
#
#     session.add(profile)
#     await session.commit()
#     print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
#     return {'user_id': user.id, 'profile_id': profile.id}

# user_profile = run(get_user_by_id_example_2(
#     username="john_doe",
#     email="john.doe@example.com",
#     password="password123",
#     first_name="John",
#     last_name="Doe",
#     age=28,
#     gender=GenderEnum.MALE,
#     profession=ProfessionEnum.ENGINEER,
#     interests=["hiking", "photography", "coding"],
#     contacts={"phone": "+123456789", "email": "john.doe@example.com"},
# ))


@connection
async def get_user_by_id_example_3(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: int | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        user = User(username=username, email=email, password=password)
        session.add(user)
        await session.flush()

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            interests=interests,
            contacts=contacts
        )
        session.add(profile)

        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()
        raise e

# user_profile = run(get_user_by_id_example_3(
#     username="Killer2009",
#     email="KingGOO.doe@example.com",
#     password="qwerty123456",
#     first_name="Ivan",
#     last_name="",
#     age=29,
#     gender=GenderEnum.MALE,
#     profession=ProfessionEnum.LAWYER,
#     interests=["velopod", "sport", "view"],
#     contacts={"phone": "+123982634", "email": "
#     KingGOO.doe@example.com"},
# ))

@connection
async def create_user_example_4(users_data: list[dict], session: AsyncSession) -> list[int]:
    users_list = [
        User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        for user_data in users_data
    ]
    session.add_all(users_list)
    await session.commit()
    return [user.id for user in users_list]

users = [
    {"username": "michael_brown", "email": "michael.brown@example.com", "password": "pass1234"},
    {"username": "sarah_wilson", "email": "sarah.wilson@example.com", "password": "mysecurepwd"},
    {"username": "david_clark", "email": "david.clark@example.com", "password": "davidsafe123"},
    {"username": "emma_walker", "email": "emma.walker@example.com", "password": "walker987"},
    {"username": "james_martin", "email": "james.martin@example.com", "password": "martinpass001"}
]

run(create_user_example_4(users_data=users))
