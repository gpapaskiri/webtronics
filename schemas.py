from typing import List

from pydantic import BaseModel, Field, EmailStr


class SetRespect(BaseModel):
    post_id: int = Field(..., description="Id поста", ge=1)


class Respect(BaseModel):
    id: int = Field(..., description="Id записи")
    user_id: int = Field(..., description="Id пользователя")
    post_id: int = Field(..., description="Id поста")
    regard: bool = Field(...)

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str = Field(..., description="Название поста")
    description: str = Field(None, description="Содержание поста")


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    id: int = Field(..., description="Id поста в базе данных", ge=1)
    title: str = Field(None, description="Название поста")


class PostDelete(BaseModel):
    id: int = Field(..., description="Id поста в базе данных", ge=1)


class Post(PostBase):
    id: int = Field(..., description="Id поста в базе данных")
    owner_id: int = Field(..., description="Id пользователя в базе данных, которому принадлежит пост")
    respects: List[Respect] = Field([], description="Список оценок пользователей")

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта, используется при регистрации и для входа")
    name: str = Field(..., description="Ник пользователя в приложении")


class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя")


class User(UserBase):
    id: int = Field(..., description="Id пользователя в базе данных")
    posts: List[Post] = Field([], description="Cписок постов пользователя")

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(..., description="Пароль пользователя")
