# FastAPI JWT Authentication

A clean, modular FastAPI backend implementation with JWT-based authentication and a PostgreSQL database. 
The project follows the **MVP (Model-View-Presenter)** architecture, providing clear separation of concerns, scalability, and maintainability.

##  Project Structure (MVP Architecture)

The application code is cleanly separated into the following layers inside the `app/` directory:

- **`models/`**: Data definitions and validation using Pydantic (`user_model.py`).
- **`views/`**: FastAPI route handlers and endpoints (`user_view.py`).
- **`presenters/`**: Core business logic, token generation, and password hashing (`auth_presenter.py`).
- **`db/`**: Database connection management and dependency injection (`database.py`).
- **`config/`**: Environment configurations and settings loading.

##  Features

- **User Registration**: Hash and store user passwords securely using `bcrypt`.
- **User Login**: Authenticate users and return access and refresh tokens.
- **Token Refresh**: Generate new access tokens using valid refresh tokens with automatic token rotation.
- **Protected Routes**: Secure endpoints requiring valid Bearer tokens (e.g., `/home`).
- **PostgreSQL Integration**: Thread-safe database connections per request.

##  Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate and retrieve JWT tokens |
| `POST` | `/refresh` | Rotate and issue a new refresh/access token pair |
| `GET` | `/home` | Example of a protected endpoint (Requires Auth) |

##  Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ankitkrrsah/fastapi-jwt-auth.git
   cd fastapi-jwt-auth
   ```

2. Set up your `.env` file in the `app/` directory:
   ```env
   SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALGORITHM=HS256
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

3. Run the development server:
   ```bash
   uvicorn app.app:app --reload
   ```
