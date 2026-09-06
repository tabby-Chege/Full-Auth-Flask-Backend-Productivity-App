# Full Auth Flask Backend - Productivity App

A Flask REST API for a productivity application with user authentication, JWT authorization, and personal notes.

## Features

* User registration and login
* Secure password hashing with Bcrypt
* JWT-based authentication
* Protected `/me` endpoint
* User-specific notes
* Full CRUD operations for notes
* Pagination for notes
* Resource ownership authorization
* Database migrations with Flask-Migrate
* Database seeding
* Automated API tests with pytest
* Protection against unauthorized access to other users' notes

## Technologies

* Python 3.12
* Flask
* Flask-RESTful
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Bcrypt
* Flask-JWT-Extended
* SQLite
* pytest

## Project Structure

```text
Full-Auth-Flask-Backend-Productivity-App/
│
├── app.py
├── config.py
├── models.py
├── seed.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── resources/
│   ├── __init__.py
│   ├── auth.py
│   └── notes.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
└── migrations/
    └── versions/
```

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:tabby-Chege/Full-Auth-Flask-Backend-Productivity-App.git
cd Full-Auth-Flask-Backend-Productivity-App
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

The application uses SQLite with Flask-SQLAlchemy and Flask-Migrate.

Initialize the migration repository if necessary:

```bash
flask --app app db init
```

Create a migration:

```bash
flask --app app db migrate -m "Create users and notes tables"
```

Apply the migration:

```bash
flask --app app db upgrade
```

## Seed the Database

To populate the database with sample users and notes:

```bash
python seed.py
```

The seed data includes four users:

* Tabby
* Prince
* Zakaria
* Wesley

The sample password for each seeded user is:

```text
password123
```

> The seeded credentials are for development and demonstration purposes only.

## Running the Application

Start the Flask development server with:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

You can also run the application using Flask:

```bash
flask --app app run
```

## API Endpoints

### Authentication

| Method | Endpoint  | Authentication | Description                          |
| ------ | --------- | -------------- | ------------------------------------ |
| POST   | `/signup` | No             | Register a new user                  |
| POST   | `/login`  | No             | Login and receive a JWT              |
| GET    | `/me`     | Yes            | Get the currently authenticated user |

### Notes

| Method | Endpoint      | Authentication | Description                        |
| ------ | ------------- | -------------- | ---------------------------------- |
| GET    | `/notes`      | Yes            | Get the authenticated user's notes |
| POST   | `/notes`      | Yes            | Create a note                      |
| GET    | `/notes/<id>` | Yes            | Get a specific note                |
| PATCH  | `/notes/<id>` | Yes            | Update a note                      |
| DELETE | `/notes/<id>` | Yes            | Delete a note                      |

## Authentication

The API uses JSON Web Tokens (JWT) to protect authenticated routes.

After logging in successfully, the API returns an access token.

Example:

```json
{
  "message": "Login successful",
  "access_token": "YOUR_JWT_TOKEN",
  "user": {
    "id": 1,
    "username": "Tabby"
  }
}
```

For protected endpoints, include the token in the `Authorization` header:

```text
Authorization: Bearer YOUR_JWT_TOKEN
```

## Example Requests

### Sign Up

```bash
curl -X POST http://127.0.0.1:5000/signup \
-H "Content-Type: application/json" \
-d '{"username":"Tabby","password":"password123"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"Tabby","password":"password123"}'
```

### Get Current User

```bash
curl http://127.0.0.1:5000/me \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create a Note

```bash
curl -X POST http://127.0.0.1:5000/notes \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{"title":"My Note","content":"My note content"}'
```

### Get Notes

```bash
curl http://127.0.0.1:5000/notes \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Pagination

Notes support pagination using `page` and `per_page` query parameters.

Example:

```text
GET /notes?page=1&per_page=10
```

Example:

```bash
curl "http://127.0.0.1:5000/notes?page=1&per_page=10" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

The response includes pagination information such as:

* Current page
* Items per page
* Total number of notes
* Total number of pages
* Whether a next page exists
* Whether a previous page exists

### Get a Single Note

```bash
curl http://127.0.0.1:5000/notes/1 \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a Note

```bash
curl -X PATCH http://127.0.0.1:5000/notes/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{"title":"Updated Title","content":"Updated content"}'
```

### Delete a Note

```bash
curl -X DELETE http://127.0.0.1:5000/notes/1 \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Authorization and Ownership

Users can only access notes that belong to them.

For example, if a note belongs to Prince, another authenticated user such as Tabby cannot:

* View the note
* Update the note
* Delete the note

Unauthorized access attempts return:

```text
403 Forbidden
```

This prevents users from accessing or modifying another user's private data.

## Password Security

Passwords are never stored as plain text.

Passwords are securely hashed using Flask-Bcrypt before being stored in the database.

The API also does not include password hashes in user responses.

## Logout

The application uses stateless JWT authentication rather than server-side sessions.

Therefore, logout is handled on the client side by removing the stored JWT access token.

## Error Handling

The API uses appropriate HTTP status codes, including:

| Status Code | Meaning                                        |
| ----------- | ---------------------------------------------- |
| 200         | Successful request                             |
| 201         | Resource created                               |
| 400         | Invalid request                                |
| 401         | Authentication required or invalid credentials |
| 403         | User does not have permission                  |
| 404         | Resource not found                             |
| 409         | Username already exists                        |

## Testing

The project includes automated API tests using pytest.

Run the test suite with:

```bash
pytest
```

The test suite covers:

* User registration
* Duplicate registration
* Password hashing
* Login
* Invalid login
* Authentication requirements
* Current user endpoint
* Note creation
* Note retrieval
* Note updates
* Note deletion
* Resource ownership
* Pagination

Expected result:

```text
14 passed
```

## Environment Configuration

The application supports configuring the JWT secret through an environment variable.

Example:

```bash
export JWT_SECRET_KEY="your-secure-secret-key"
```

A development fallback secret is provided in `config.py` for local development.

For production deployments, use a strong secret stored securely in the environment rather than committing secrets to source control.

## Development Notes

The SQLite database is stored inside the Flask `instance/` directory.

The database and virtual environment are excluded from Git using `.gitignore`.

Database migration files are committed so that the database schema can be recreated in another environment.

## Project Status

The Full Auth Flask Backend - Productivity App is complete and includes:

* JWT authentication
* Secure password hashing
* Protected resources
* User ownership authorization
* Notes CRUD functionality
* Pagination
* Database migrations
* Seed data
* Automated tests
* Project documentation
