from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactResponse

from sqlalchemy import and_, or_

from datetime import datetime, timedelta

from sqlalchemy import extract
import calendar


def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]


async def get_contacts(user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )


async def get_contacts_got_birthday(user: User, db: Session) -> List[Contact]:
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    return (
        db.query(Contact)
        .filter(
            and_(
                or_(
                    and_(
                        extract("month", Contact.born_date) == today.month,
                        extract("day", Contact.born_date) >= today.day,
                        or_(
                            and_(
                                extract("month", Contact.born_date)
                                == extract("month", next_week),
                                extract("day", Contact.born_date) <= next_week.day,
                            ),
                            extract("month", Contact.born_date)
                            != extract("month", next_week),
                        ),
                    ),
                    and_(
                        extract("month", Contact.born_date)
                        == extract("month", next_week),
                        extract("day", Contact.born_date) <= next_week.day,
                    ),
                ),
                Contact.user_id == user.id,
            )
        )
        .all()
    )


async def get_contacts_with_string(
    search_by: str, user: User, db: Session
) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(
            and_(
                (
                    Contact.forename.ilike(f"%{search_by}%")
                    | Contact.surname.ilike(f"%{search_by}%")
                    | Contact.email.ilike(f"%{search_by}%")
                ),
                Contact.user_id == user.id,
            )
        )
        .all()
    )


async def create_contact(body: ContactResponse, user: User, db: Session) -> Contact:
    contact = Contact(
        forename=body.forename,
        surname=body.surname,
        email=body.email,
        phone_number=body.phone_number,
        born_date=body.born_date,
        user_id=user.id,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
    contact_id: int, body: ContactResponse, user: User, db: Session
) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        contact.forename = body.forename
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.born_date = body.born_date

        db.commit()
    return contact
