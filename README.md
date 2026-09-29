# Social Logistics Platform

A FastAPI backend for a logistics and delivery platform. The project provides a foundation for managing customers, delivery agents, delivery requests, delivery status changes, authentication, payments, notifications, tracking, and webhook integrations.

> **Project status:** This repository is an active backend project. The core authentication and delivery flows are implemented, while several supporting modules and integrations are still being expanded.

## Overview

The platform is designed around a delivery lifecycle that moves a shipment through controlled states:

```text
REQUESTED → ACCEPTED → PICKED_UP → IN_TRANSIT → DELIVERED
     └──────────────→ CANCELLED
```

A delivery cannot move backward or skip invalid states. `DELIVERED` and `CANCELLED` are terminal states.

## Features

- FastAPI application with automatic OpenAPI documentation
- Async SQLAlchemy/SQLModel database access
- PostgreSQL development environment through Docker Compose
- Alembic database migrations
- User registration and login endpoints
- Password hashing with Argon2
- JWT access-token generation
- Delivery creation, listing, and updates
- Delivery status validation through a state machine
- Health-check endpoint
- Request-ID and timing middleware
- Pytest test suite using an isolated SQLite database
- GitHub Actions CI with PostgreSQL, migrations, and tests
- Integration placeholders for email, Firebase, payments, Redis, and webhooks

## Technology Stack

- **Python** 3.11+
- **FastAPI** and **Uvicorn**
- **SQLModel** with async SQLAlchemy
- **PostgreSQL** for local development and production-style database work
- **Alembic** for migrations
- **JWT** with PyJWT
- **Argon2** for password hashing
- **Redis** configuration support
- **Pytest**, `pytest-asyncio`, and HTTPX for testing
- **Docker Compose** for the local PostgreSQL service

## Project Structure

```text
.
├── app/
│   ├── core/             # Configuration and security helpers
│   ├── db/               # Async database engine and sessions
│   ├── integrations/     # Email, Firebase, and payment integration modules
│   ├── middleware/       # Request-ID and timing middleware
│   ├── models/           # Database models
│   ├── repositories/     # Database access abstractions
│   ├── routers/          # HTTP API routes
│   ├── schemas/          # Request and response schemas
│   └── services/         # Business logic and delivery state machine
├── alembic/              # Database migration environment and revisions
├── tests/                # API and service tests
├── .env.example          # Environment-variable template
├── docker-compose.yml    # Local PostgreSQL service
├── pyproject.toml        # Project and dependency metadata
└── uv.lock               # Locked dependency resolution
```

## Requirements

Install the following before starting:

- Python 3.11 or newer
- Docker and Docker Compose
- Git

You can use either `uv` or a standard Python virtual environment. The commands below use a virtual environment and `pip` so they work in more environments.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Abigail56/social-logistics-platform.git
cd social-logistics-platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install application and development dependencies

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev]"
```

### 4. Start PostgreSQL

The included Compose file starts PostgreSQL on host port `5436`:

```bash
docker compose up -d postgres
```

Check that the service is healthy:

```bash
docker compose ps
```

### 5. Configure environment variables

Copy the example file and review the values:

```bash
cp .env.example .env
```

The default local configuration is:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5436/social_logistics
JWT_SECRET=replace-with-a-random-secret-at-least-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REDIS_URL=redis://localhost:6379/0
```

For any shared or deployed environment, replace the database credentials and generate a strong, private JWT secret. Never commit `.env` or real credentials.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, open:

- Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- ReDoc: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)
- OpenAPI JSON: [`http://127.0.0.1:8000/openapi.json`](http://127.0.0.1:8000/openapi.json)

## API Reference

### Health

```http
GET /health
```

Returns the service health status:

```json
{
  "status": "healthy",
  "service": "social-logistics-api"
}
```

### Authentication

#### Register a user

```http
POST /auth/register
Content-Type: application/json
```

Example request:

```json
{
  "email": "user@example.com",
  "username": "demo-user",
  "password": "use-a-strong-password",
  "role": "customer"
}
```

#### Log in

```http
POST /auth/login
Content-Type: application/json
```

Example request:

```json
{
  "username": "demo-user",
  "password": "use-a-strong-password"
}
```

Both endpoints return a token response when successful. Review the schema definitions in `app/schemas/auth.py` for the exact accepted fields and response shape.

### Deliveries

#### List deliveries

```http
GET /deliveries/
```

#### Create a delivery

```http
POST /deliveries/
Content-Type: application/json
```

Example request:

```json
{
  "customer_id": 1,
  "pickup_location": "Lagos",
  "destination": "Ibadan",
  "package_details": "Books",
  "total_amount": 2500
}
```

New deliveries start in the `REQUESTED` state.

#### Update a delivery

```http
PATCH /deliveries/{delivery_id}
Content-Type: application/json
```

Example status update:

```json
{
  "status": "ACCEPTED"
}
```

Allowed statuses are:

- `REQUESTED`
- `ACCEPTED`
- `PICKED_UP`
- `IN_TRANSIT`
- `DELIVERED`
- `CANCELLED`

Invalid status transitions return a `400` response. A missing delivery returns `404`.

### Supporting routes

The project also exposes initial route groups for future expansion:

- `GET /users/`
- `GET /agents/`
- `GET /payments/`
- `POST /webhooks/`

These modules currently contain lightweight placeholder behavior and should be treated as work in progress.

## Running Tests

The test suite uses an isolated SQLite database, so local tests do not require the Docker PostgreSQL service:

```bash
pytest -q
```

To run a specific test module:

```bash
pytest -q tests/test_delivery_state_machine.py
```

## Continuous Integration

GitHub Actions runs on pushes to `main` and `master`, and on pull requests. The workflow:

1. Starts PostgreSQL 16
2. Installs Python 3.11
3. Installs application and development dependencies
4. Applies Alembic migrations
5. Runs `pytest -q`

The workflow is defined in `.github/workflows/ci.yml`.

## Database Migrations

Create a migration after changing database models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Review autogenerated migrations carefully before applying them. Apply migrations with:

```bash
alembic upgrade head
```

To roll back one migration:

```bash
alembic downgrade -1
```

## Security Notes

- Use a unique JWT secret of at least 32 characters outside local development.
- Keep `.env` files and credentials out of version control.
- Do not use the sample PostgreSQL password in production.
- Validate and authorize access to delivery, payment, and user resources before deploying publicly.
- Review webhook authentication and payment-provider verification before enabling external integrations.

## Roadmap

Potential next steps for the platform include:

- Add authentication and role-based authorization to protected routes
- Complete agent assignment and delivery tracking workflows
- Add pagination, filtering, and ownership checks to list endpoints
- Implement payment and notification integrations behind explicit interfaces
- Add webhook signature verification and idempotency handling
- Add API versioning and richer error responses
- Add deployment documentation and environment-specific configuration
- Expand integration, authorization, and failure-path test coverage

## Contributing

1. Create a feature branch from `main`.
2. Make a focused change with tests where practical.
3. Run `pytest -q` locally.
4. Run database migrations locally if models changed.
5. Open a pull request with a clear summary and testing notes.

## License

No license has been declared yet. Add a `LICENSE` file before presenting this repository as reusable open-source software.
