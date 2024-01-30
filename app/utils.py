from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas
from .database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify_login(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def generate_pwd_from_email(email:str):
    username, domain = email.split("@")
    first_name = username[0].upper()
    last_name = username.split(".")[1].lower()
    generated_password = first_name[0] + last_name + "@gsl"

    return generated_password


def save_email_to_db(subject, body, to_email, is_sent=False, error_details=None):
    db = SessionLocal()
    email = models.Email(subject=subject, body=body, to_email=to_email, is_sent=is_sent, error_details=error_details)
    db.add(email)
    db.commit()


def create_user(db: Session, user: schemas.UserCreate):
    password_gen = generate_pwd_from_email(user.email)

    hashed_password = hash(password_gen)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_role_id=user.user_role_id,
        signature_url=user.signature_url,
        image_url=user.image_url
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    body = f'Hello {db_user.name},\nYour details have been successfully created in the Job Card Portal.\n\nTo login, use the following credentials.\nUsername : {db_user.email}\nPassword : {password_gen}\n\nFor any inquiries, please consult the support desk.\n\nBest regards,\nThe Support Team'
    save_email_to_db("Password Change Notification", body, db_user.email)
    return db_user


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def create_user_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int):
    db_ticket = models.Ticket(**ticket.dict(), consultant_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_user_roles(db: Session, skip: int=0, limit:int=100):
    return db.query(models.UserRole).offset(skip).limit(limit).all()

def get_user_role_by_name(db: Session, rolename: str):
    return db.query(models.UserRole).filter(models.UserRole.name == rolename).first()

def get_unsent_emails(db: Session, limit:int=100):
    return db.query(models.Email).filter(models.Email.is_sent == False).limit(limit).all()

def get_email_config(db: Session):
    return db.query(models.EmailConfig).filter(models.EmailConfig.is_active == True).first()