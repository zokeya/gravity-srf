from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
  prefix = "/mailconfig",
  tags = ["Mail Config"]
)


@router.get("/")
def get_email_config(
  db: Session = Depends(get_db),
  admin_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):
    mail_config = db.query(models.EmailConfig).first()
    return mail_config

@router.post("/", response_model=schemas.MailConfig)
def create_email_config(
  config: schemas.MailConfig,
  db: Session = Depends(get_db)
  ,current_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):
    db_config = models.EmailConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.put("/{id}", response_model=schemas.MailConfig)
def update_email_config(
  id:int,
  config: schemas.MailConfig,
  db: Session = Depends(get_db),
  current_user: schemas.User = Depends(oauth2.get_current_adminuser)
  ):

  mailconfig_query = db.query(models.EmailConfig).filter(models.Email.id == id)
  mailconfig = mailconfig_query.first()

  if not mailconfig:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mail confifuration with id of {id} was not found")

  mailconfig_query.update(config.dict(), synchronize_session=False)
  db.commit()

  db.refresh(mailconfig)
  return mailconfig