from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional

from .. import models, schemas, utils, oauth2, mailer
from ..database import get_db

router = APIRouter(
  prefix = "/users",
  tags = ["Users"]
)


@router.post("/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
    ):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return utils.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
    ):
    users = utils.get_users(db, skip=skip, limit=limit)
    return users


@router.put("/reset_pwd", response_model=schemas.UserLogin)
def reset_pwd_login_user(
    login_user: schemas.UserLoginResetModel,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)):

  if not utils.verify_login(login_user.oldpassword, current_user.password):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Provided Old password is invalid"
    )

  hashed_password = utils.hash(login_user.newpassword)

  # Update the user's password in the database
  current_user.password = hashed_password
  db.commit()

  body = f'Hello {current_user.name},Your password has been changed successfully.\n\n Your new Password is; {login_user.newpassword}\n\nFor any inquiries, please consult the support desk.\nBest regards,\nThe Support Team'
  utils.save_email_to_db("Password Change Notification", body, current_user.email)

  return current_user


@router.put("/admin_reset_pwd/{user_id}/{auto_gen_pwd}", response_model=schemas.UserLogin)
def reset_pwd_admin(
    user_id: int,
    auto_gen_pwd: bool,
    user_data: Optional[schemas.UserLogin] = None,
    db: Session = Depends(get_db),
    admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
):
    try:
        # Retrieve the user from the database
        db_user = utils.get_user(db, user_id=user_id)

        # Check if the user exists
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # If auto_gen_pwd is True, generate a new password and update the user's password
        if auto_gen_pwd:
            password_gen = utils.generate_pwd_from_email(db_user.email)
            hashed_password = utils.hash(password_gen)
            db_user.password = hashed_password
            body = f'Hello {db_user.name},\nYour password has been changed successfully.\n\n Your new Password is; {password_gen}\n\nFor any inquiries, please consult the support desk.\n\nBest regards,\nThe Support Team'
        else:
            # If a new password is provided, hash and update the user's password
            hashed_password = utils.hash(user_data.password)
            db_user.password = hashed_password
            body = f'Hello {db_user.name},\nYour password has been changed successfully.\n\n Your new Password is; {user_data.password}\n\nFor any inquiries, please consult the support desk.\n\nBest regards,\nThe Support Team'

        # Commit the changes to the database
        db.commit()
        utils.save_email_to_db("Password Change Notification", body, db_user.email)

        # Return the updated user information
        return db_user
    except Exception as e:
        # If an exception occurs, rollback the transaction
        db.rollback()
        raise e  # Re-raise the exception after rollback


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
    ):
    db_user = utils.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/tickets/", response_model=schemas.Ticket)
def create_ticket_for_user(
    user_id: int, ticket: schemas.TicketCreate, db: Session = Depends(get_db)
):
    return utils.create_user_ticket(db=db, ticket=ticket, user_id=user_id)


@router.put("/{id}")
def update_user(
        id: int,
        updated_user: schemas.UserCreate,
        db: Session = Depends(get_db),
        admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
    ):
  user_query = db.query(models.User).filter(models.User.id == id)

  user = user_query.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id of {id} was not found")

  user_query.update(updated_user.dict(), synchronize_session=False)

  db.commit()

  return {"data" : user_query.first()}


