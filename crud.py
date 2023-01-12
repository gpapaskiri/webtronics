import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
import schemas


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.Users(email=user.email, hashed_password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.Users:
    return db.query(models.Users).filter(models.Users.email == email).first()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Posts(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def edit_user_post(db: Session, post: schemas.PostUpdate):
    db_post = db.query(models.Posts).filter(models.Posts.id == post.id).first()
    db_post.title = post.title
    db_post.description = post.description
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_user_post(db: Session, post: models.Posts):
    db.delete(post)
    db.commit()
    return True


def get_user_post(db: Session, post_id: int) -> models.Posts:
    return db.query(models.Posts).filter(models.Posts.id == post_id).first()


def get_posts(db: Session):
    return db.query(models.Posts).all()


def like_post(db: Session, respect: schemas.SetRespect, user_id: int):
    db_respect = models.Respects(**respect.dict(), user_id=user_id, regard=True)
    db.add(db_respect)
    db.commit()
    db.refresh(db_respect)
    return db_respect


def dislike_post(db: Session, respect: schemas.SetRespect, user_id: int):
    db_respect = models.Respects(**respect.dict(), user_id=user_id, regard=False)
    db.add(db_respect)
    db.commit()
    db.refresh(db_respect)
    return db_respect


def check_respect(db: Session, post_id: int, user_id: int):
    return db.query(models.Respects).filter(
        and_(models.Respects.post_id == post_id, models.Respects.user_id == user_id)).first()
