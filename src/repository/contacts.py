from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactResponse

from datetime import datetime, timedelta

from sqlalchemy import extract
import calendar

def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

async def get_contacts(db: Session) -> List[Contact]:
    return db.query(Contact).all()

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contacts_got_birthday(db: Session) -> List[Contact]:
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    days_in_this_month = days_in_month(today.year, today.month)

    return db.query(Contact).filter(
        (
            (extract('month', Contact.born_date) == today.month) &
            (extract('day', Contact.born_date) >= today.day) &
            (extract('day', Contact.born_date) <= next_week.day)
        ) |
        (
            (extract('month', Contact.born_date) > today.month) &
            (extract('month', Contact.born_date) == next_week.month) &
            (days_in_this_month - extract('day', Contact.born_date) <= next_week.day))
        ).all()

async def get_contacts_with_string(search_by: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        (
            Contact.forename.ilike(f"%{search_by}%") |
            Contact.surname.ilike(f"%{search_by}%") |
            Contact.email.ilike(f"%{search_by}%")
        )
    ).all()


async def create_contact(body: ContactResponse, db: Session) -> Contact:
    contact = Contact(
        forename=body.forename,
        surname=body.surname,
        email=body.email,
        phone_number=body.phone_number,
        born_date = body.born_date
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactResponse, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.forename = body.forename
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.born_date = body.born_date

        db.commit()
    return contact
