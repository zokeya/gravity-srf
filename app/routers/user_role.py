from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
  prefix = "/roles",
  tags = ["User Roles"]
)

@router.get("/", response_model=list[schemas.UserRole])
def get_user_roles(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_db)):
    user_roles = utils.get_user_roles(db, skip=skip, limit=limit)
    return user_roles


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRole)
def create_user_role(
  user_role: schemas.UserRoleBase,
  db: Session = Depends(get_db),
  admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):

  db_user_role = utils.get_user_role_by_name(db, rolename=user_role.name)

  if db_user_role:
    raise HTTPException(status_code=400, detail=f"User Role with the name {db_user_role.name} already exists")

  new_user_role = models.UserRole(**user_role.dict())
  db.add(new_user_role)
  db.commit()
  db.refresh(new_user_role)
  return new_user_role

@router.get("/{id}")
async def get_userole(
    id: int,
    db: Session = Depends(get_db),
    admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):
  urole = db.query(models.UserRole).filter(models.UserRole.id == id).first()
  if not urole:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User Role with id of {id} was not found")

  return {"data" : urole}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(
    id: int,
    db: Session = Depends(get_db),
    admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):
  userRole = db.query(models.UserRole).filter(models.UserRole.id == id)

  if userRole.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Role with id of {id} was not found")

  userRole.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_user_role(
    id: int,
    updated_urole: schemas.UserRoleBase,
    db: Session = Depends(get_db),
    admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):
  urole_query = db.query(models.UserRole).filter(models.UserRole.id == id)

  ticket = urole_query.first()

  if not ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Role with id of {id} was not found")

  urole_query.update(updated_urole.dict(), synchronize_session=False)
  db.commit()

  return {"data" : urole_query.first()}