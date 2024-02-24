
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

<br>

<br>

# Homework #12

In this homework assignment, we continue working on the RESTful API application from the previous homework assignment.

## Tasks
- Implement an authentication mechanism;
- Implement an authorization mechanism using JWT tokens, so that all operations on contacts are performed only by registered users;
- Users should only have access to their own contact operations.

## General Requirements
- If a user with the given email address already exists during registration, the server should return an HTTP 409 Conflict error;
- The server hashes the password and does not store it in the database in plain text;
- In the case of successful user registration, the server should return an HTTP 201 Created response status and the data of the new user;
- In the case of successful POST requests used to create new resources, the server returns a 201 Created status;
- For POST requests used for user authentication, the server accepts requests with user data (email, password) in the body of the request;
- If the user does not exist or the password is incorrect, the system returns an HTTP 401 Unauthorized error;
- The authorization mechanism is implemented using a pair of JWT tokens: an access token (`access_token`) and a refresh token (`refresh_token`).

