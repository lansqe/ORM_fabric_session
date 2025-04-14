from typing import Optional, Annotated, List, Dict
import enum
from sqlalchemy import ForeignKey, String, JSON, text, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql_enums import GenderEnum, RatingEnum, ProfessionEnum, StatusPost
from database import Base, uniq_str_un, array_or_none_an, content_an  # Оптимизировано путем аннотации

class User(Base):
    username: Mapped[uniq_str_un]
    email: Mapped[uniq_str_un]
    password: Mapped[str]

    # Связь один-к-одному с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Обеспечивает связь один-к-одному
        lazy="joined"  # Автоматически загружает связанные данные из Profile при запросе User
    )

    # Связь один-ко-многим с Post
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Post
    )

    # Связь один-ко-многим с Comment
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Comment
    )


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(default=ProfessionEnum.DEVELOPER,
                                                       server_default=text("'UNEMPLOYED'"))
    interests: Mapped[array_or_none_an]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    # Обратная связь один-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )


class Post(Base):
    title: Mapped[str]
    content: Mapped[content_an]
    main_photo_url: Mapped[str]
    photos_url: Mapped[array_or_none_an]
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    # Связь один-ко-многим с Comment
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    content: Mapped[content_an]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))

    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    # Связь многие-к-одному с Post
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )


