from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by their email address.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email address, or None if not found.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user with the given user data and generates an avatar URL using Gravatar.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user with an avatar URL.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a given user.

    :param user: The user to update the token for.
    :type user: User
    :param token: The new refresh token. Can be None to remove the token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Marks a user's email as confirmed.

    :param email: The email address of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Updates the avatar URL for a user identified by their email address.

    :param email: The email address of the user to update the avatar for.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
