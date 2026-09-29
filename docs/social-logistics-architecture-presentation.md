# Social Logistics Platform — Architecture Presentation

This 10-slide structure is based on the current implementation in the repository. It distinguishes implemented components from work-in-progress integrations and placeholder routes.

## Slide 1 — Title and system purpose

**Title:** Social Logistics Platform Architecture

**Key message:** A FastAPI backend foundation for logistics and delivery workflows.

**Include:**

- Project purpose and current implementation status
- Core technologies: Python, FastAPI, SQLModel, PostgreSQL, Alembic
- Repository link and API documentation link

## Slide 2 — Architecture at a glance

**Key message:** The platform follows a layered API architecture.

**Diagram:**

```text
Client / API Consumer
        |
        v
FastAPI Routers + OpenAPI
        |
        v
Schemas → Services → Repositories
        |         |
        v         v
  Domain Models  State Machine
        |
        v
Async Database Session → PostgreSQL
```

**Mention:** Request-ID and timing middleware wrap incoming requests.

## Slide 3 — Application structure

**Key message:** The codebase separates transport, business logic, persistence, and infrastructure concerns.

**Show:**

- `app/routers/` — HTTP route groups
- `app/schemas/` — request and response contracts
- `app/services/` — business rules
- `app/repositories/` — persistence abstractions
- `app/models/` — SQLModel entities
- `app/core/` and `app/db/` — configuration and database setup
- `app/integrations/` — external-service boundaries

## Slide 4 — Request lifecycle

**Key message:** Requests move through predictable middleware, routing, validation, service, and persistence stages.

**Flow:**

```text
HTTP request
  → Request ID middleware
  → Timing middleware
  → Router
  → Pydantic / SQLModel validation
  → Service or repository logic
  → Async database session
  → Response model
```

**Highlight:** FastAPI automatically exposes Swagger UI, ReDoc, and OpenAPI JSON.

## Slide 5 — Authentication and security foundation

**Key message:** Authentication is implemented as a JWT-based foundation, with additional authorization hardening planned.

**Cover:**

- `POST /auth/register`
- `POST /auth/login`
- Argon2 password hashing
- PyJWT access-token generation
- Configurable token expiration
- Environment-based JWT secret and algorithm

**Important note:** Protected-route authorization and role-based access control remain roadmap work.

## Slide 6 — Delivery domain and state machine

**Key message:** Delivery status changes are explicitly controlled by a domain state machine.

**State flow:**

```text
REQUESTED → ACCEPTED → PICKED_UP → IN_TRANSIT → DELIVERED
     └──────────────→ CANCELLED
```

**Explain:**

- Invalid transitions are rejected
- `DELIVERED` and `CANCELLED` are terminal states
- Delivery updates validate state changes before persistence
- The model supports a clear path for audit history and notifications

## Slide 7 — Data and persistence architecture

**Key message:** Async persistence and migrations support local development and production-style workflows.

**Cover:**

- SQLModel models with async SQLAlchemy sessions
- PostgreSQL 16 through Docker Compose
- Host development port `5436`
- Alembic migration environment
- SQLite-backed isolated test fixtures
- Repository classes for database access

**Show:** Example entities including users, deliveries, tracking, payments, ratings, disputes, and notifications.

## Slide 8 — API surface and integration boundaries

**Key message:** The API exposes core delivery functionality while leaving clear boundaries for future integrations.

**Current route groups:**

- `/health`
- `/auth/`
- `/deliveries/`
- `/users/`
- `/agents/`
- `/payments/`
- `/webhooks/`

**Work-in-progress boundaries:**

- Email
- Firebase
- Payments
- Redis-backed services
- Webhook verification and idempotency

## Slide 9 — Quality, delivery, and operational workflow

**Key message:** Automated checks provide a repeatable baseline for changes.

**CI flow:**

```text
Push / Pull Request
        ↓
PostgreSQL service
        ↓
Python 3.11 setup
        ↓
Install application + dev dependencies
        ↓
Alembic upgrade head
        ↓
pytest -q
```

**Mention:** Local tests use an isolated SQLite database; deployment-specific secrets must never be committed.

## Slide 10 — Roadmap and architecture priorities

**Key message:** The current foundation is ready for deeper authorization, workflow, and operational capabilities.

**Priorities:**

1. Add route authentication and role-based authorization
2. Complete agent assignment and delivery tracking
3. Add pagination, filtering, and ownership checks
4. Implement payment and notification providers behind interfaces
5. Add webhook signatures and idempotency
6. Add API versioning, deployment guidance, and broader failure-path tests

**Closing statement:** The architecture is intentionally modular so the platform can grow from a tested backend foundation into a complete logistics system.
