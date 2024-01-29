from typing import Annotated

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
  prefix = "/posts",
  tags = ["Posts"]
)

@router.get("/", response_model=list[schemas.Post])
def get_posts(
  current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_db)):
    posts = utils.get_posts(db, skip=skip, limit=limit)
    return posts

# @router.get("/")
# def get_posts(db: Session = Depends(get_db)):
#   posts = db.query(models.Post).all()
#   return {"data" : posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
  post: schemas.PostCreate,
  db: Session = Depends(get_db),
  current_user: schemas.User = Depends(oauth2.get_current_user)
  # current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]
  ):

  new_post = models.Post(user_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  my_post = db.query(models.Post).filter(models.Post.id == id).filter(models.Post.user_id == current_user.id).first()
  if not my_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id of {id} was not found")
  return {"data" : my_post}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id of {id} was not found")

  post.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  post = post_query.first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id of {id} was not found")

  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()

  return {"data" : post_query.first()}