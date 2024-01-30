from pydantic import BaseModel
from pydantic.types import conint
from datetime import datetime

class TicketBase(BaseModel):
    # description: str | None = None
    company_name: str
    contact_person: str
    application: str
    version: str
    start_date: datetime
    start_time: datetime
    end_date: datetime
    end_time: datetime
    problem_reported: str
    diagnosis: str
    solution_provided: str
    total_hrs: str
    chargeable: bool
    amount: str


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    consultant_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    name: str
    user_role_id: int


class UserCreate(UserBase):
    signature_url: str | None = None
    image_url: str | None = None
    is_active: bool | None = None

class User(UserBase):
    id: int
    name: str
    signature_url: str | None = None
    image_url: str | None = None
    is_active: bool
    tickets: list[Ticket] = []

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResetModel(BaseModel):
    oldpassword: str
    newpassword: str

class UsernameResetModel(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    useremail: str | None = None


class UserRoleBase(BaseModel):
    name: str

class UserRole(UserRoleBase):
    id: int
    users: list[User] = []

    class Config:
        orm_mode = True

class MailConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: str
    is_active: bool