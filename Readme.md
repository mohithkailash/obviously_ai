# Books API - obviously.ai take home

A FastAPI application providing CRUD operations for books with JWT authentication.

## Features

- User Authentication with JWT
- CRUD operations for Books
- Custom Exception Handling
- Input Validation using Pydantic
- SQLite Database with SQLAlchemy ORM

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── exception_types.py
│   │   └── handlers.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── user.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       └── books.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohithkailash/obviously_ai.git
cd obviously_ai
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## API Endpoints

### Authentication

- POST `/api/auth/register`

  - Register a new user
  - Body: `{"username": "string", "password": "string"}`

- POST `/api/auth/login`
  - Login to get access token
  - Form data: `username`, `password`

### Books

All book endpoints require authentication (Bearer token)

- GET `/api/books`

  - Get all books (paginated)
  - Query parameters:
    - skip (default: 0)
    - limit (default: 10, max: 100)

- GET `/api/books/{book_id}`

  - Get a specific book

- POST `/api/books`

  - Create a new book
  - Body:
    ```json
    {
      "title": "string",
      "author": "string",
      "published_date": "date",
      "summary": "string",
      "genre": "string"
    }
    ```

- PATCH `/api/books/{book_id}`

  - Update a book
  - Body: Same as POST, all fields optional

- DELETE `/api/books/{book_id}`
  - Delete a book

## Exception Handling

The API implements custom exception handling for:

- Not Found errors
- Authentication errors
- Duplicate entry errors
- Database errors
- Validation errors

## Authentication Flow

1. Register a new user using `/api/auth/register`
2. Login using `/api/auth/login` to get a JWT token
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer <your-token>
   ```

## Database

The application uses SQLite as the database:

- Database file: `books.db`
- ORM: SQLAlchemy
- Models automatically created on startup

## Development

- Exception handling is centralized
- Input validation using Pydantic models
- Database operations use SQLAlchemy ORM
- Authentication using JWT tokens
