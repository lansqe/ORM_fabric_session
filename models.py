from typing import Optional, Annotated, List, Dict
import enum
from sqlalchemy import ForeignKey, String, JSON, text, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql_enums import GenderEnum, RatingEnum, ProfessionEnum, StatusPost
from database import Base, uniq_str_un, array_or_none_an  # Оптимизировано путем аннотации

class User(Base):
    username: Mapped[uniq_str_un] # Тут
    email: Mapped[uniq_str_un] # И тут
    password: Mapped[str]
    profile_id: Mapped[Optional[int]] = mapped_column(ForeignKey('profiles.id'))

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user", # Атрибут обратной связи(указывает на user)
        uselist=False, # Ключевой параметр для связи один-к-одному
                       # По умолчанию relationship предполагает связь "один-ко-многим" или "многие-к-одному".
                       # uselist=False задает связь 1к1
        lazy="joined" # Автоматически подгружает profile при запросе user
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user", # связывает с полем user в Post
        cascade="all, delete-orphan" # Удаляет посты при удалении пользователя
    )

    comments: Mapped["Comment"] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    age: Mapped[Optional[int]]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    contacts: Mapped[Optional[Dict]] = mapped_column(JSON)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile", # относится к профилю
        uselist=False # 1k1
    )

class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    main_photo_url: Mapped[str]
    photos: Mapped[Optional[List[Text]]] = mapped_column(ARRAY(String))
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts" # указывает на связь с полем posts в User.
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(
        default=RatingEnum.FIVE,
        server_default=text("'SEVEN'")
    )

    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="user"
    )

    # Связь многие-к-одному с Post
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )


