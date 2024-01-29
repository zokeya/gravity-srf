from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, utils, oauth2

router = APIRouter(
  tags=["Auth"]
)

@router.post("/login/", response_model=schemas.Token)
def login(user_credentidals: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
  user = utils.get_user_by_email(db, user_credentidals.username)

  if not user:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Invalid credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )

  if not utils.verify_login(user_credentidals.password, user.password):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Invalid credentials"
    )

  # access_token = oauth2.create_access_token(data={"user_id" : user.id})
  access_token = oauth2.create_access_token(data={"username" : user.email})

  return {"access_token" : access_token, "token_type" : "bearer"}


@router.put("/forgot_pwd/", response_model=schemas.UserLogin)
def reset_password(
    user_credentials: schemas.UsernameResetModel,
    db: Session = Depends(database.get_db)
):
# Check if the user with the specified email exists
  user = utils.get_user_by_email(db, user_credentials.username)
  if not user:
    raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="User with the specified email does not exist",
          headers={"WWW-Authenticate": "Bearer"},
      )

  # Generate a new password
  password_gen = utils.generate_pwd_from_email(user.email)

  # Hash the new password securely
  hashed_password = utils.hash(password_gen)

  # Update the user's password in the database
  user.password = hashed_password
  db.commit()

  # Return a response model with only necessary information
  return user