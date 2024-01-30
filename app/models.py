from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import datetime

from .database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="user_role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    signature_url = Column(String)
    image_url = Column(String)
    user_role_id = Column(Integer, ForeignKey("user_roles.id"))
    is_active = Column(Boolean, default=True, nullable=False)

    tickets = relationship("Ticket", back_populates="user")

    user_role = relationship("UserRole", back_populates="users")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True, nullable=False)
    contact_person = Column(String, index=True, nullable=False)
    application = Column(String, index=True, nullable=False)
    version = Column(String, index=True, nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.now().date())
    start_time = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    end_date = Column(DateTime, nullable=False, default=datetime.datetime.now().date())
    end_time = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    problem_reported = Column(String, index=True, nullable=False)
    diagnosis = Column(String, index=True, nullable=False)
    solution_provided = Column(String, index=True, nullable=False)
    total_hrs = Column(Numeric, index=True, nullable=False)
    amount = Column(Float, index=True)
    chargeable = Column(Boolean, default=False, nullable=False)
    consultant_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="tickets")


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    is_sent = Column(Boolean, default=False)
    error_details = Column(String, nullable=True)
    sent_date = Column(String, server_default=func.now())


class EmailConfig(Base):
    __tablename__ = "email_config"

    id = Column(Integer, primary_key=True, index=True)
    smtp_server = Column(String)
    smtp_port = Column(Integer)
    smtp_username = Column(String)
    smtp_password = Column(String)
    sender_email = Column(String)
    is_active = Column(Boolean, default=True)
