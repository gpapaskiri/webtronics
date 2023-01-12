import sys

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import auth_handler
import crud
import models
import schemas
from auth_bearer import JWTBearer
from auth_handler import signJWT
from config import get_config
from database import engine, SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login")
async def login(user: schemas.Login, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    if not crud.check_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    return signJWT(db_user.id)


@app.post("/logout")
async def logout():
    pass


@app.get("/post/{post_id}", response_model=schemas.Post)
async def get_post(post_id, db: Session = Depends(get_db)):
    result = crud.get_user_post(db, post_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No post with id {post_id}")
    return result


@app.get("/post")
async def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)


@app.post("/post", dependencies=[Depends(JWTBearer())])
async def create_post(post: schemas.PostCreate, request: Request, db: Session = Depends(get_db)):
    user_id = auth_handler.get_user(request.headers['authorization'].split(' ')[-1])
    if user_id is None:
        return HTTPException(status_code=401, detail="Unable authorize, try re-login")
    return crud.create_user_post(db, post=post, user_id=user_id)


@app.put("/post", dependencies=[Depends(JWTBearer())])
async def edit_post(post: schemas.PostUpdate, request: Request, db: Session = Depends(get_db)):
    user_id = auth_handler.get_user(request.headers['authorization'].split(' ')[-1])
    if user_id is None:
        return HTTPException(status_code=401, detail="Unable authorize, try re-login")
    db_post = crud.get_user_post(db, post.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"No post with id {post.id}")
    if db_post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Attempt to edit someone else's post")
    if post.title is None and post.description is None:
        raise HTTPException(status_code=400, detail="Nothing change. Recieved title and description for post are empty")
    return crud.edit_user_post(db, post)


@app.delete("/post", dependencies=[Depends(JWTBearer())])
async def delete_post(post: schemas.PostDelete, request: Request, db: Session = Depends(get_db)):
    user_id = auth_handler.get_user(request.headers['authorization'].split(' ')[-1])
    if user_id is None:
        return HTTPException(status_code=401, detail="Unable authorize, try re-login")
    db_post = crud.get_user_post(db, post.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"No post with id {post.id}")
    if db_post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Attempt to delete someone else's post")
    crud.delete_user_post(db, db_post)
    return {"message": "Post is deleted"}


@app.post("/like", dependencies=[Depends(JWTBearer())])
async def like_post(respect: schemas.SetRespect, request: Request, db: Session = Depends(get_db)):
    user_id = auth_handler.get_user(request.headers['authorization'].split(' ')[-1])
    if user_id is None:
        return HTTPException(status_code=401, detail="Unable authorize, try re-login")
    db_post = crud.get_user_post(db, respect.post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"No post with id {respect.post_id}")
    if db_post.owner_id == user_id:
        raise HTTPException(status_code=403, detail="Unable like your own post")
    if crud.check_respect(db, respect.post_id, user_id):
        raise HTTPException(status_code=403, detail="Available only one vote for every post")
    return crud.like_post(db, respect, user_id)


@app.post("/dislike", dependencies=[Depends(JWTBearer())])
async def dislike_post(respect: schemas.SetRespect, request: Request, db: Session = Depends(get_db)):
    user_id = auth_handler.get_user(request.headers['authorization'].split(' ')[-1])
    if user_id is None:
        return HTTPException(status_code=401, detail="Unable authorize, try re-login")
    db_post = crud.get_user_post(db, respect.post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"No post with id {respect.post_id}")
    if db_post.owner_id == user_id:
        raise HTTPException(status_code=403, detail="Unable dislike your own post")
    if crud.check_respect(db, respect.post_id, user_id):
        raise HTTPException(status_code=403, detail="Available only one vote for every post")
    return crud.dislike_post(db, respect, user_id)


if __name__ == "__main__":
    try:
        sys.argv[1]
    except:
        uvicorn.run("main:app", **get_config("uvicorn"))
    else:
        models.Base.metadata.create_all(bind=engine)
