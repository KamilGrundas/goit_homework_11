from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactResponse

from sqlalchemy import and_, or_

from datetime import datetime, timedelta

from sqlalchemy import extract
import calendar


def days_in_month(year: int, month: int) -> int:
    """
    Returns the number of days in a given month of a specific year.

    :param year: The year of the month to check.
    :type year: int
    :param month: The month to check.
    :type month: int
    :return: Number of days in the specified month and year.
    :rtype: int
    """
    return calendar.monthrange(year, month)[1]


async def get_contacts(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user.

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )


async def get_contacts_got_birthday(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user whose birthdays are coming up within the next week.

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts with upcoming birthdays.
    :rtype: List[Contact]
    """
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
    """
    Retrieves a list of contacts for a specific user that match a search string in their name or email.

    :param search_by: The string to search by in the contact's name or email.
    :type search_by: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts matching the search criteria.
    :rtype: List[Contact]
    """
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
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactResponse
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
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
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
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
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactResponse
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
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
