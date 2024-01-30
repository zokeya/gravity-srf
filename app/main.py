from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas, utils, mailer
from .database import engine
from .routers import user_role,auth, user, ticket, mail_config

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user_role.router)
app.include_router(user.router)
app.include_router(ticket.router)
app.include_router(mail_config.router)

@app.get("/")
async def root():
  return {"message": "Hello there!"}

@app.get("/sendmail")
async def send_emails():
  mailer.send_unsent_emails()


