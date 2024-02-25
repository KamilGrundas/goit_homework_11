from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactResponse, ContactBase
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of all contacts for the currently authenticated user.

    :param current_user: The user whose contacts are to be retrieved, obtained via token authentication.
    :param db: Dependency injection for the database session.
    :return: A list of contact response models.
    """
    contacts = await repository_contacts.get_contacts(current_user, db)
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_contacts_got_birthday(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve contacts of the currently authenticated user with upcoming birthdays within the next week.

    :param current_user: The user whose contacts are to be retrieved, obtained via token authentication.
    :param db: Dependency injection for the database session.
    :return: A list of contact response models with upcoming birthdays.
    """
    contacts = await repository_contacts.get_contacts_got_birthday(current_user, db)
    return contacts


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    search_by: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Search for contacts by a given string in the name, phone number, or email.

    :param search_by: The string to search for in the contacts.
    :param current_user: The user performing the search, obtained via token authentication.
    :param db: Dependency injection for the database session.
    :return: A list of contact response models that match the search criteria.
    """
    contacts = await repository_contacts.get_contacts_with_string(
        search_by, current_user, db
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieve a single contact by ID for the currently authenticated user.

    :param contact_id: The unique identifier of the contact to retrieve.
    :param db: Dependency injection for the database session.
    :param current_user: The user attempting to retrieve the contact, obtained via token authentication.
    :return: The contact response model if found, otherwise an HTTP 404 error.
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Create a new contact for the currently authenticated user.

    :param body: The contact information to be created.
    :param db: Dependency injection for the database session.
    :param current_user: The user creating the contact, obtained via token authentication.
    :return: The newly created contact response model.
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    body: ContactBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Update an existing contact for the currently authenticated user.

    :param contact_id: The unique identifier of the contact to update.
    :param body: The updated contact information.
    :param db: Dependency injection for the database session.
    :param current_user: The user updating the contact, obtained via token authentication.
    :return: The updated contact response model.
    """
    contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Delete an existing contact for the currently authenticated user.

    :param contact_id: The unique identifier of the contact to delete.
    :param db: Dependency injection for the database session.
    :param current_user: The user deleting the contact, obtained via token authentication.
    :return: The deleted contact response model if successful, otherwise an HTTP 404 error.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
