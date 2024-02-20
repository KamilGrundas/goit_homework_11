
# Homework #11

The goal of this homework assignment is to create a REST API interface for storing and managing contacts. The API should be built using the FastAPI framework and use SQLAlchemy for database management.

Contacts should be stored in the database and contain the following information:

- First Name
- Last Name
- Email Address
- Phone Number
- Date of Birth
- Additional Information (optional)

The API should be capable of performing the following actions:

- Create a new contact
- Retrieve a list of all contacts
- Retrieve one contact by ID
- Update an existing contact
- Delete a contact

In addition to basic functionality, the CRUD API should also have the following features:

- Contacts should be searchable by first name, last name, or email address (Query).
- The API should be able to retrieve a list of contacts with birth dates in the next 7 days.

## General Requirements

- Use of the FastAPI framework for creating the API.
- Use of SQLAlchemy ORM for working with the database.
- PostgreSQL should be used as the database.
- Support for CRUD operations for contacts.
- Support for storing the contact's date of birth.
- Provision of documentation for the API.
- Use of the Pydantic data validation module.
