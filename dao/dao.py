from dao.base import BaseDAO
from models import User, Profile, Post, Comment


class UserDAO(BaseDAO):
    model = User


class ProfileDAO(BaseDAO):
    model = Profile


class PostDAO(BaseDAO):
    model = Post


class CommentDAO(BaseDAO):
    model = Comment
