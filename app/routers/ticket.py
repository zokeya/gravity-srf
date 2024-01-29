from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
  prefix = "/tickets",
  tags = ["Tickets"]
)

@router.get("/", response_model=list[schemas.Ticket])
def read_tickets(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_db),
  current_user: schemas.User = Depends(oauth2.get_current_user)):
    tickets = utils.get_tickets(db, skip=skip, limit=limit)
    return tickets


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ticket)
def create_ticket(
  ticket: schemas.TicketCreate,
  db: Session = Depends(get_db),
  current_user: schemas.User = Depends(oauth2.get_current_user)
  ):

  new_ticket = models.Ticket(consultant_id=current_user.id, **ticket.dict())
  db.add(new_ticket)
  db.commit()
  db.refresh(new_ticket)
  return new_ticket

@router.get("/{id}")
async def get_ticket(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  my_ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
  if not my_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ticket with id of {id} was not found")

  if my_ticket.consultant_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ticket with id of {id} does not belong to you")

  return {"data" : my_ticket}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  ticket = db.query(models.Ticket).filter(models.Ticket.id == id)

  if ticket.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with id of {id} was not found")

  if ticket.first().consultant_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with id of {id} does not belong to you and hence cannot be deleted")

  ticket.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_ticket(id: int, updated_ticket: schemas.TicketCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  ticket_query = db.query(models.Ticket).filter(models.Ticket.id == id).filter(models.Ticket.consultant_id == current_user.id)

  ticket = ticket_query.first()

  if not ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with id of {id} was not found")

  ticket_query.update(updated_ticket.dict(), synchronize_session=False)
  db.commit()

  return {"data" : ticket_query.first()}